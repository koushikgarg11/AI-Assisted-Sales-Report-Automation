def generate_insights(df):

    insights = []

    if "Category" in df.columns and "Sales" in df.columns:

        top_category = df.groupby("Category")["Sales"].sum().idxmax()

        insights.append(
            f"{top_category} category generates the highest revenue."
        )

    if "Region" in df.columns and "Sales" in df.columns:

        top_region = df.groupby("Region")["Sales"].sum().idxmax()

        insights.append(
            f"{top_region} region contributes the highest sales."
        )

    if "Sales" in df.columns:

        avg_sales = df["Sales"].mean()

        insights.append(
            f"Average sales value per transaction is {round(avg_sales,2)}."
        )

    if "Sales" in df.columns:

        max_sale = df["Sales"].max()

        insights.append(
            f"The highest recorded transaction is {max_sale}."
        )

    return insights
