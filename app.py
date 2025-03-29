import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="E-commerce Sales Insights", layout='wide')

st.markdown("""
## 🔍 Business Insights Summary

- **Cluster 0** makes up 20% of customers but contributes 50% of total revenue → focus retention efforts here.
- **Cluster 3** shows high recency but low spend → consider upselling or re-engagement campaigns.
- **Cluster 4** are new customers → provide onboarding discounts or loyalty programs.
""")


@st.cache_data
def load_data():
    df = pd.read_csv("outputs/rfm_segmented.csv")
    return df


df = load_data()


st.sidebar.title("Filter Options")
clusters = sorted(df['Cluster'].unique())
selected_clusters = st.sidebar.multiselect(
    "Select Cluster(s)", clusters, default=clusters)


customer_id = st.sidebar.text_input("Search CustomerID")

st.sidebar.markdown("**Select Charts to Display**")
selected_charts = st.sidebar.multiselect(
    "Choose charts",
    [
        "Recency Distribution",
        "Monetary Distribution",
        "Cluster Scatter Plot",
        "Pie Chart - Cluster Distribution",
        "Bar Chart - Avg RFM",
        "Box Plot - Monetary by Cluster"
    ],
    default=[
        "Recency Distribution",
        "Monetary Distribution",
        "Cluster Scatter Plot"
    ]
)

# Filter data
filtered_df = df[df['Cluster'].isin(selected_clusters)]

if customer_id:
    filtered_df = filtered_df[filtered_df['CustomerID'].astype(
        str).str.contains(customer_id)]


st.title("E-commerce RFM customer Segmentation")

st.write(f"Showing {len(filtered_df)} customers")
st.dataframe(filtered_df)

st.download_button("Download filtered data", filtered_df.to_csv(
    index=False), file_name='filtered_rfm.csv')

st.markdown("Cluster Overview")
cluster_summary = filtered_df.groupby('Cluster').agg({
    "Recency": 'mean',
    "Frequency": 'mean',
    "Monetary": 'mean',
    "CustomerID": 'count'
}).rename(columns={"CustomerID": 'Count'}).reset_index()

st.dataframe(cluster_summary)

st.markdown("Visualize Cluster Distribution")

if "Recency Distribution" in selected_charts or "Monetary Distribution" in selected_charts:
    col1, col2 = st.columns(2)

    if "Recency Distribution" in selected_charts:
        with col1:
            fig1, ax1 = plt.subplots()
            sns.histplot(filtered_df['Recency'], kde=True, ax=ax1)
            ax1.set_title("Recency Distribution")
            st.pyplot(fig1)

    if "Monetary Distribution" in selected_charts:
        with col2:
            fig2, ax2 = plt.subplots()
            sns.histplot(filtered_df['Monetary'], kde=True, ax=ax2)
            ax2.set_title("Monetary Distribution")
            st.pyplot(fig2)


if "Cluster Scatter Plot" in selected_charts:
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='Recency', y='Monetary',
                    hue='Cluster', palette='tab10', ax=ax3)
    ax3.set_title("Clusters by Recency and Monetary")
    st.pyplot(fig3)

if "Pie Chart - Cluster Distribution" in selected_charts:
    cluster_counts = filtered_df['Cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', "Count"]
    fig4 = px.pie(cluster_counts, values='Count', names='Cluster',
                  title="Cluster Distribution by Segment")
    st.plotly_chart(fig4)

if "Bar Chart - Avg RFM" in selected_charts:
    avg_rfm = filtered_df.groupby(
        'Cluster')[['Recency', 'Frequency', 'Monetary']].mean().reset_index().round()
    fig5 = px.bar(avg_rfm, x='Cluster', y=['Recency', 'Frequency', 'Monetary'],
                  barmode='group', title='Average RFM Values per Cluster')
    st.plotly_chart(fig5)

if "Box Plot - Monetary by Cluster" in selected_charts:
    fig6 = px.box(filtered_df, x='Cluster', y='Monetary',
                  title='Monetary Distribution per Cluster')
    st.plotly_chart(fig6)
