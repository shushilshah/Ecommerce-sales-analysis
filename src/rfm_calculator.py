from datetime import timedelta


def calculate_rfm(df):
    snapshot_date = df['InvoiceNo'].max() + timedelta(days=1)

    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum',
    }).reset_index()

    rfm.columns = ['CustomerID', 'Recency',
                   'Frequency', 'Monetary']

    return rfm
