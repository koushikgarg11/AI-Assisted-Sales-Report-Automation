import pandas as pd


def generate_insights(df):

    insights = []

    columns = [c.lower() for c in df.columns]

    # Detect possible sales column
    sales_col = None
    for col in df.columns:
        if col.lower() in ["sales", "revenue", "amount", "profit"]:
            sales_col = col

    # Detect region column
    region_col = None
    for col in df.columns:
        if col.lower() in ["region", "location", "state"]:
            region_col = col

    # Detect category column
    category_col = None
    for col in df.columns:
        if col.lower() in ["category", "product category", "product"]:
            category_col = col

    # Top Region
    if sales_col and region_col:

        top_region = (
            df.groupby(region_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

        insights.append(f"{top_region} region generated the highest revenue.")

    # Top Category
    if sales_col and category_col:

        top_category = (
            df.groupby(category_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

        insights.append(f"{top_category} is the best performing product category.")

    # Total Sales Insight
    if sales_col:

        total_sales = df[sales_col].sum()

        insights.append(f"Total sales across dataset is ${total_sales:,.0f}.")

    return insights
