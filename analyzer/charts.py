import matplotlib.pyplot as plt
import io
import base64



#функция превращения графика в пнг картинку а затем в превращает в текстовую base64 строку(для html отчета)

def _fig_to_base64(fig):   
    buffer = io.BytesIO()#создание области памяти чтобы сохранить картинку для html отчета
    fig.savefig(buffer, format="png")#сохранение в пнг
    plt.close(fig)#освобождение памяти
    buffer.seek(0)  #перемотка курсора в начало буфера, чтобы прочитать его с начала
    return base64.b64encode(buffer.read()).decode("utf-8")


#MTTR по категориям.
def mttr_bytype(mttr_series):
    fig, ax = plt.subplots(figsize=(8, 5))   # холст (fig) и оси (ax) 
    mttr_series.plot(kind="bar", ax=ax, color="#4C72B0")  #столбчатая диаграмма

    ax.set_title("Average MTTR by Ticket Type")
    ax.set_xlabel("Ticket Type")
    ax.set_ylabel("Hours")
    plt.xticks(rotation=45, ha="right")#поворт подписей по оси х
    plt.tight_layout()  #автоматически подгоняет отступы

    return _fig_to_base64(fig)


#SLA compliance 
def sla_compliance(sla_series):
    fig, ax = plt.subplots(figsize=(6, 6))
    sla_series.plot(kind="pie", ax=ax, autopct="%1.1f%%", colors=["#5ADF79", "#CC3D42"])  #pie круговая диаграмма  показывает процент на секторах диаграммы, .цифра%".

    ax.set_title("SLA Compliance")
    ax.set_ylabel("")
    plt.tight_layout()

    return _fig_to_base64(fig)



#Распределение по приоритету/каналу 
def priority_distribution(priority_series):
    fig, ax = plt.subplots(figsize=(8, 5))
    priority_series.plot(kind="bar", ax=ax, color="#52DD91")

    ax.set_title("Tickets by Priority")
    ax.set_xlabel("Priority")
    ax.set_ylabel("Number of Tickets")
    plt.xticks(rotation=0)
    plt.tight_layout()

    return _fig_to_base64(fig)


def priority_cchannel(priority_channel):
    fig, ax = plt.subplots(figsize=(8, 5))
    priority_channel.plot(kind="bar", ax=ax, color="#5D5BE0")

    ax.set_title("Tickets by Channel")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Number of Tickets")
    plt.xticks(rotation=0)
    plt.tight_layout()

    return _fig_to_base64(fig)


#Тикеты по часам heatmap(df) 
def heatmap_chart(heatmap_series):

    fig, ax = plt.subplots(figsize=(8, 5))
    heatmap_series.plot(kind="line", ax=ax, color="#E48E3D")

    ax.set_title("Heatmap by hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Count of Tickets")
    plt.xticks(rotation=0)
    plt.tight_layout()

    return _fig_to_base64(fig)
