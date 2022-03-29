
import uuid, base64
from io import BytesIO
from matplotlib import pyplot
# chart = get_chart(chart_type, sales_df, results_by)
def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
def get_chart():#chart_type, data, results_by, **kwargs
    # pyplot.switch_backend('AGG')
    fig = pyplot.figure(figsize=(10, 4))
    # key = get_key(results_by)
    # d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    pyplot.plot([1,2,3],[0.3,.5,0.2],color='gray', marker='o', linestyle='dashed')
    # if chart_type == '#1':
    #     print("Bar graph")
    #     pyplot.bar(d[key], d['total_price'])
    #    # seaborn.barplot(x=key, y='total_price', data=d)
    # elif chart_type == '#2':

    #     print("Pie chart")
    #     pyplot.pie(data=d,x='total_price', labels=d[key])
    # elif chart_type == '#3':
    #     print("Line graph")
    #     pyplot.plot(d[key], d['total_price'], color='gray', marker='o', linestyle='dashed')
    # else:
    #     print("Apparently...chart_type not identified")
    pyplot.tight_layout()
    chart = get_graph()
    return chart