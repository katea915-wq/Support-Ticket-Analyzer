import pandas as pd
from analyzer.loader import load_tickets

df = load_tickets("data/tickets.csv")

#время закрытия в чачсах закрытых тикетов
def timeclosedtickets(df: pd.DataFrame):  
    closed = df[
    (df["ticket_status"] == "Closed") &
    (df["time_to_resolution"] >= df["first_response_time"])
].copy()
    closed["mttr"] = closed["time_to_resolution"] - closed["first_response_time"]
# Время закрытия в часах
    closed["timeclose"] = closed["mttr"].dt.total_seconds() / 3600
    return closed


#Среднее время закрытия (MTTR) по категориям  (ticket_type)
def mttr(df):  
    closedtime = timeclosedtickets(df)
    return closedtime.groupby("ticket_type")["timeclose"].mean()


#Были ли выполнены тикеты воворемя
def slacheck(df): 
    closedtime = timeclosedtickets(df)
    SLA_LIMITS = {
    "Low": 72,
    "Medium": 48,
    "High": 24,
    "Critical": 8
}
    closedtime["sla_limit"] = closedtime["ticket_priority"].map(SLA_LIMITS)  #берёт колонку ticket_priority целиком и для каждого значения ищет соответствие в словаре, возвращая новую колонку sla_limit
    closedtime["sla_status"] = closedtime["timeclose"] <= closedtime["sla_limit"] #True False

    closedtime["SLA"] = closedtime["sla_status"].map({
        True: "Closed in time",
        False: "Closed not in time"
    })

    return closedtime[["ticket_priority", "timeclose", "sla_limit", "sla_status", "SLA"]]


#распределение тикетов по приоритету и по каналу (ticket_channel)

def distribution(df):
    priority_distribution = df["ticket_priority"].value_counts()
    channel_distribution = df["ticket_channel"].value_counts()
    return priority_distribution, channel_distribution

#Топ n самых долгих тикетов

def longtime(df,n):
    closedtime = timeclosedtickets(df)
    return closedtime.sort_values("timeclose", ascending=False).head(n)

##Количество тикетов  по часам 
def heatmap(df):
    closedtime = timeclosedtickets(df)
    closedtime["hour"] = closedtime["first_response_time"].dt.hour   #first_response_time (когда тикет реально появился в системе)    .dt.hour. достать час
    return closedtime.groupby("hour").size()  #подсчет количества строк в каждой группе

