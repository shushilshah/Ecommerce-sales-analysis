import pandas as pd


def load_clean_data(filepath):
    df = pd.read_excel(filepath)

    df.columns = df.columns.str.strip()
    # drop rows for missing customerID
    df.dropna(subset=['CustomerID'], inplace=True)
    # Remove canceled orders
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df['InvoiceNo'] = pd.to_datetime(df['InvoiceDate'])

    # create totalprice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    return df
