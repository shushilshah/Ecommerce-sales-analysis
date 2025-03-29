from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def cluster_customers(rfm_df, n_clusters=4):
    features = rfm_df[['Recency', 'Frequency', 'Monetary']]
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = model.fit_predict(rfm_scaled)
    rfm_df['Cluster'] = cluster_labels

    return rfm_df
