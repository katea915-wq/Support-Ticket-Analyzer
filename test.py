import logging
from analyzer.loader import load_tickets
from analyzer.metrics import distribution,mttr,slacheck,longtime,heatmap
from analyzer.charts import mttr_bytype, sla_compliance,priority_distribution, priority_cchannel,heatmap_chart
from templates.report import generate_report
import base64


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


###########################проверка создается ли картинка как надо  (типо iVBORw0KGgoAAAANSUhE.........)
img_mttr = mttr_bytype(mttr(df))
img_sla = sla_compliance(slacheck(df)["SLA"].value_counts())

priority_dist, channel_dist = distribution(df)
img_priority = priority_distribution(priority_dist)
img_channel = priority_cchannel(channel_dist)

img_heatmap = heatmap_chart(heatmap(df))

print("All charts generated:", all([img_mttr, img_sla, img_priority, img_channel, img_heatmap]))

with open("test_chart.png", "wb") as f:
    f.write(base64.b64decode(img_mttr))

path = generate_report(df, "report.html")
print(f"Report saved to {path}")