import plotly.express as px

def generate_chart(df, x, y, chart_type):

    if chart_type == "bar":
        fig = px.bar(df, x=x, y=y)

    elif chart_type == "line":
        fig = px.line(df, x=x, y=y)

    elif chart_type == "scatter":
        fig = px.scatter(df, x=x, y=y)

    elif chart_type == "box":
        fig = px.box(df, x=x, y=y)

    elif chart_type == "histogram":
        fig = px.histogram(df, x=y)

    elif chart_type == "pie":
        fig = px.pie(df, names=x, values=y)

    else:
        fig = px.bar(df, x=x, y=y)

    return fig
