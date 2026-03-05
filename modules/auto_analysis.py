def detect_columns(df):

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

    return numeric_cols, cat_cols
