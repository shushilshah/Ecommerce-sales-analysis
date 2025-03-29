import matplotlib.pyplot as plt
import seaborn as sns


def plot_rfm_distributions(rfm):
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    sns.histplot(rfm['Recency'], bins=20, kde=True, ax=axs[0])

    axs[0].set_title("Recency Distribution")

    sns.histplot(rfm['Frequency'], bins=20, kde=True, ax=axs[1])
    axs[1].set_title("Frequecy Distribution")

    sns.histplot(rfm['Monetary'], bins=20, kde=True, ax=axs[2])
    axs[2].set_title("Monetary Distribution")
    plt.tight_layout()
    plt.show()


def plot_clusters(rfm, x='Recency', y='Monetary'):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=rfm, x=x, y=y, hue='Cluster', palette='tab10')
    plt.title(f"Customer Segments by {x} and {y}")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend(title="Cluster")
    plt.grid(True)
    plt.show()
