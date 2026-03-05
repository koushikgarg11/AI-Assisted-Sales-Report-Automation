def clean_data(df):

    df = df.drop_duplicates()

    df = df.fillna("Unknown")

    return df
