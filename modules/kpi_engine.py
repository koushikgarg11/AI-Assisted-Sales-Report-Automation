import pandas as pd


def generate_kpis(df):

    kpis = {}

    # numeric columns
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return kpis

    main_metric = numeric_cols[0]

    kpis["Total Revenue"] = df[main_metric].sum()
    kpis["Total Orders"] = len(df)
    kpis["Average Order Value"] = df[main_metric].mean()

    # find categorical columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(cat_cols) > 0:
        top_category = df.groupby(cat_cols[0])[main_metric].sum().idxmax()
        kpis["Top Category"] = top_category

    if len(cat_cols) > 1:
        top_region = df.groupby(cat_cols[1])[main_metric].sum().idxmax()
        kpis["Top Region"] = top_region

    return kpis
