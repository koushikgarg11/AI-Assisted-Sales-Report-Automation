import plotly.express as px


def find_column(df, possible_names):
    for col in df.columns:
        if col.lower() in possible_names:
            return col
    return None


def sales_by_region(df):

    region_col = find_column(df, ["region", "location", "state", "area"])
    sales_col = find_column(df, ["sales", "revenue", "amount", "total"])

    if not region_col or not sales_col:
        return None

    data = df.groupby(region_col)[sales_col].sum().reset_index()

    fig = px.bar(
        data,
        x=region_col,
        y=sales_col,
        title="Sales by Region"
    )

    return fig


def sales_by_category(df):

    category_col = find_column(df, ["category", "product category", "product"])
    sales_col = find_column(df, ["sales", "revenue", "amount", "total"])

    if not category_col or not sales_col:
        return None

    data = df.groupby(category_col)[sales_col].sum().reset_index()

    fig = px.bar(
        data,
        x=category_col,
        y=sales_col,
        title="Sales by Category"
    )

    return fig


def sales_trend(df):

    date_col = find_column(df, ["order date", "date"])
    sales_col = find_column(df, ["sales", "revenue", "amount", "total"])

    if not date_col or not sales_col:
        return None

    df[date_col] = df[date_col].astype("datetime64[ns]")

    data = df.groupby(date_col)[sales_col].sum().reset_index()

    fig = px.line(
        data,
        x=date_col,
        y=sales_col,
        title="Sales Trend Over Time"
    )

    return fig
