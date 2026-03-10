import plotly.express as px

def sales_by_region(df):

    fig = px.bar(
        df.groupby("Region")["Sales"].sum().reset_index(),
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    return fig


def sales_by_category(df):

    fig = px.pie(
        df,
        names="Category",
        values="Sales",
        title="Sales by Category"
    )

    return fig


def sales_trend(df):

    if "Order Date" in df.columns:

        df["Order Date"] = df["Order Date"].astype("datetime64")

        trend = df.groupby("Order Date")["Sales"].sum().reset_index()

        fig = px.line(trend, x="Order Date", y="Sales", title="Sales Trend")

        return fig
