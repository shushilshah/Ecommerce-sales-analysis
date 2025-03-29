from src.data_loader import load_clean_data
from src.rfm_calculator import calculate_rfm
from src.clustering import cluster_customers
from src.visualizations import plot_rfm_distributions, plot_clusters


def main():
    df = load_clean_data("data/Online Retail.xlsx")

    rfm = calculate_rfm(df)

    # plot_rfm_distributions(rfm)

    rfm_clustered = cluster_customers(rfm, n_clusters=4)

    rfm_clustered.to_csv("outputs/rfm_segmented.csv", index=False)
    print("RFM clustering completed and saved to outputs/rfm_segmented.csv ")

    # plot_clusters(rfm_clustered, x='Recency', y='Monetary')

    # plot_clusters(rfm_clustered, x='Frequency', y='Monetary')


if __name__ == "__main__":
    main()
