def generate_kpis(df):

    kpis = {}

    if "Sales" in df.columns:
        kpis["Total Revenue"] = df["Sales"].sum()

    if "Order ID" in df.columns:
        kpis["Total Orders"] = df["Order ID"].nunique()

    if "Sales" in df.columns and "Order ID" in df.columns:
        kpis["Average Order Value"] = df["Sales"].sum() / df["Order ID"].nunique()

    if "Category" in df.columns:
        kpis["Top Category"] = df.groupby("Category")["Sales"].sum().idxmax()

    if "Region" in df.columns:
        kpis["Top Region"] = df.groupby("Region")["Sales"].sum().idxmax()

    return kpis
