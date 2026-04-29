import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Dashboard Looker Studio (Olist)", layout="wide")

# --- CHARGEMENT ---
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "olist_looker.csv")
    df = pd.read_csv(path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

st.title("Tableau de Bord Looker Studio (Réplique Streamlit)")
st.markdown("---")

# --- 6. FILTRE GLOBAL ---
categories = sorted(df['product_category_name'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Filtrer par catégorie", ["Toutes"] + categories)

if selected_category != "Toutes":
    df_filtered = df[df['product_category_name'] == selected_category]
else:
    df_filtered = df

# --- 1 & 2. SCORECARDS ---
col1, col2 = st.columns(2)
with col1:
    total_ca = df_filtered['price'].sum()
    st.metric("Chiffre d'Affaires Total", f"${total_ca:,.2f}")
with col2:
    nb_orders = df_filtered['order_id'].nunique()
    st.metric("Nombre de commandes", f"{nb_orders:,}")

st.divider()

# --- 3. TOP 10 CATÉGORIES ---
st.subheader("Top 10 catégories par CA")
top_cat = df_filtered.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(10).reset_index()
fig_cat = px.bar(top_cat, x='price', y='product_category_name', orientation='h', color='price', color_continuous_scale='Blues')
fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_cat, use_container_width=True)

# --- 4. ÉVOLUTION CA PAR MOIS ---
st.subheader("Évolution CA par mois")
df_filtered['month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M').astype(str)
evolution = df_filtered.groupby('month')['price'].sum().reset_index()
fig_line = px.line(evolution, x='month', y='price', markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# --- 5. CA PAR ÉTAT ---
st.subheader("CA par état (seller_state)")
state_ca = df_filtered.groupby('seller_state')['price'].sum().sort_values(ascending=False).reset_index()
fig_state = px.bar(state_ca, x='seller_state', y='price', color='price', color_continuous_scale='Viridis')
st.plotly_chart(fig_state, use_container_width=True)
