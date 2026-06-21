from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from analyzer.metrics import mttr, slacheck, distribution, longtime, heatmap
from analyzer.charts import mttr_bytype, sla_compliance,priority_distribution, priority_cchannel,heatmap_chart

def generate_report(df, output_path="report.html"):
    priority_dist, channel_dist = distribution(df)

    context = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "img_mttr": mttr_bytype(mttr(df)),
        "img_sla": sla_compliance(slacheck(df)["SLA"].value_counts()),
        "img_priority": priority_distribution(priority_dist),
        "img_channel": priority_cchannel(channel_dist),
        "img_heatmap": heatmap_chart(heatmap(df)),
        "top_tickets": longtime(df, 10).to_dict(orient="records"),
    }

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")
    html = template.render(context)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path