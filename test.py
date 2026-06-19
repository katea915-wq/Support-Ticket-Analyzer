import logging
from analyzer.loader import load_tickets
from analyzer.metrics import distribution,mttr,slacheck,longtime,heatmap

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

df = load_tickets("data/tickets.csv")
print(df.dtypes)
print(df.head(3))
print(df["ticket_status"].value_counts())


#--------------------------------
print("\n Average closing time by category:")
print(mttr(df))

print("\n SLA Check:")
print(slacheck(df))

print("\n Tickets distribution:")
priority_dist, channel_dist = distribution(df)
print(priority_dist)
print(channel_dist)

print("\n Most long tickets:")
print(longtime(df, 10))

print("Count of tickets by the hour")
print(heatmap(df))