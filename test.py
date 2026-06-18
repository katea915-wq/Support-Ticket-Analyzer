import logging
from analyzer.loader import load_tickets

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

df = load_tickets("data/tickets.csv")
print(df.dtypes)
print(df.head(3))
print(df["ticket_status"].value_counts())