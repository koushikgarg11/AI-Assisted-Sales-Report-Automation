import plotly.express as px


def sales_by_region(df):

    numeric_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(numeric_cols) == 0 or len(cat_cols) == 0:
        return None

    metric = numeric_cols[0]
    category = cat_cols[0]

    data = df.groupby(category)[metric].sum().reset_index()

    fig = px.bar(data, x=category, y=metric, title=f"{metric} by {category}")

    return fig


def sales_by_category(df):

    numeric_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(numeric_cols) == 0 or len(cat_cols) < 2:
        return None

    metric = numeric_cols[0]
    category = cat_cols[1]

    data = df.groupby(category)[metric].sum().reset_index()

    fig = px.bar(data, x=category, y=metric, title=f"{metric} by {category}")

    return fig


def sales_trend(df):

    numeric_cols = df.select_dtypes(include="number").columns
    date_cols = df.select_dtypes(include="datetime").columns

    if len(numeric_cols) == 0 or len(date_cols) == 0:
        return None

    metric = numeric_cols[0]
    date_col = date_cols[0]

    data = df.groupby(date_col)[metric].sum().reset_index()

    fig = px.line(data, x=date_col, y=metric, title=f"{metric} Trend")

    return fig
