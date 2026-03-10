import pandas as pd


def load_data(uploaded_file):

    try:
        # Try reading as UTF-8 first
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="utf-8")

        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        else:
            raise ValueError("Unsupported file format")

    except UnicodeDecodeError:

        # If UTF-8 fails, try latin1 (common fix)
        df = pd.read_csv(uploaded_file, encoding="latin1")

    return df
