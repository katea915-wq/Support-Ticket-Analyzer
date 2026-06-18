import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

critical_columns = ["ticket_id", "date_of_purchase", "time_to_resolution"]
date_columns = ["date_of_purchase", "time_to_resolution", "first_response_time"]

def load_tickets(filepath: str) -> pd.DataFrame:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not Found: {filepath}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected CSV-file, received: {path.suffix}")

    logger.info(f"Downloading data from {filepath}")
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")   #нужно в строку перевести т.к тип "индекс"

    missing = [col for col in critical_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
        
    for col in date_columns:
        if col in df.columns: #проверка есть ли значение в датафрейме   
            df[col] = pd.to_datetime(df[col], errors="coerce")  #перевод в дату и если не получается распарсить как дату, то NaT
            nulls = df[col].isna().sum()  #Считаем сколько NaT появилось после конвертации
            if nulls > 0:
                logger.warning(f"'{col}': {nulls} values are not parsed as a date")

    before = len(df)
    df = df.dropna(subset=["ticket_id"]).drop_duplicates(subset=["ticket_id"])  #df.dropna(subset=["ticket_id"]) - выбрасывает строки где пустая дата
#drop_duplicates(subset=["ticket_id"]) - выбрасывает строки где ticket_id повторяется

    dropped = before - len(df)
    if dropped:
        logger.warning(f"Deleted {dropped} rows (null ticket_id or duplicate)")

    logger.info(f"Tickets loaded: {len(df)}")
    return df