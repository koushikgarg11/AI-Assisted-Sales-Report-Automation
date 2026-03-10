def generate_insights(df):

    insights = []

    numeric_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(numeric_cols) == 0:
        return insights

    metric = numeric_cols[0]

    total = df[metric].sum()
    avg = df[metric].mean()

    insights.append(f"Total {metric} across dataset is {total:,.2f}.")
    insights.append(f"Average {metric} per record is {avg:,.2f}.")

    if len(cat_cols) > 0:

        top_cat = df.groupby(cat_cols[0])[metric].sum().idxmax()

        insights.append(
            f"{top_cat} contributes the highest {metric}."
        )

    return insights
