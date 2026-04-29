import streamlit as st
import polars as pl
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Performance Commerciale — Analyse Retail Olist",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES AVEC CACHE ---
@st.cache_data
def load_and_prepare_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "..", "data")
    
    # Chargement Polars
    orders = pl.read_csv(os.path.join(DATA_PATH, "olist_orders_dataset.csv"))
    items = pl.read_csv(os.path.join(DATA_PATH, "olist_order_items_dataset.csv"))
    products = pl.read_csv(os.path.join(DATA_PATH, "olist_products_dataset.csv"))
    sellers = pl.read_csv(os.path.join(DATA_PATH, "olist_sellers_dataset.csv"))
    
    # Requête DuckDB
    query = """
    SELECT 
        i.order_id,
        date_trunc('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS purchase_month,
        i.product_id,
        COALESCE(p.product_category_name, 'inconnue') AS category,
        i.seller_id,
        i.price
    FROM items i
    JOIN orders o ON i.order_id = o.order_id
    LEFT JOIN products p ON i.product_id = p.product_id
    JOIN sellers s ON i.seller_id = s.seller_id
    WHERE o.order_status = 'delivered'
    """
    
    df = duckdb.query(query).pl()
    return df

df = load_and_prepare_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.markdown("""
    Analyse de la performance commerciale d'une 
    plateforme e-commerce : CA, vendeurs, catégories.
    """)
    st.divider()

st.title("Performance Commerciale — Analyse Retail Olist")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyse Produits & Vendeurs", "Simulateur de CA"])

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    col1, col2 = st.columns(2)
    
    ca_total = df['price'].sum()
    ca_moyen = df.group_by('order_id').agg(pl.sum('price'))['price'].mean()
    
    col1.metric("Chiffre d'Affaires Total", f"${ca_total:,.2f}")
    col2.metric("Chiffre d'Affaires Moyen par Commande", f"${ca_moyen:,.2f}")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Catégories par CA")
        cat_ca = df.group_by('category').agg(pl.sum('price').alias('total_ca')).sort('total_ca', descending=True).head(10).to_pandas()
        fig_cat = px.bar(cat_ca, x='total_ca', y='category', orientation='h', color='total_ca', color_continuous_scale='Blues')
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with c2:
        st.subheader("Évolution Mensuelle du CA")
        timeline = df.group_by('purchase_month').agg(pl.sum('price').alias('total_ca')).sort('purchase_month').to_pandas()
        # Formattage de la date
        timeline['purchase_month'] = timeline['purchase_month'].dt.strftime('%Y-%m')
        fig_time = px.line(timeline, x='purchase_month', y='total_ca', markers=True)
        st.plotly_chart(fig_time, use_container_width=True)


# --- ONGLET 2 : PRODUITS & VENDEURS ---
with tab2:
    categories_list = df['category'].unique().to_list()
    selected_category = st.selectbox("Filtrer par catégorie", ["Toutes"] + categories_list)
    
    if selected_category == "Toutes":
        df_filtered = df
    else:
        df_filtered = df.filter(pl.col('category') == selected_category)
        
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Top Vendeurs par Chiffre d'Affaires**")
        top_sellers = df_filtered.group_by('seller_id').agg(pl.sum('price').alias('total_ca')).sort('total_ca', descending=True).head(10).to_pandas()
        st.dataframe(top_sellers, use_container_width=True)
        
    with c2:
        st.write("**Vendeurs Sous-Performants (CA < Moyenne)**")
        avg_ca = df_filtered.group_by('seller_id').agg(pl.sum('price').alias('total_ca'))['total_ca'].mean()
        bad_sellers = df_filtered.group_by('seller_id').agg(pl.sum('price').alias('total_ca')).filter(pl.col('total_ca') < avg_ca).sort('total_ca', descending=False).head(10).to_pandas()
        st.dataframe(bad_sellers, use_container_width=True)
        
    st.write("**Scatter Plot : Volume vs CA par Catégorie**")
    cat_analysis = df.group_by('category').agg([
        pl.mean('price').alias('avg_price'),
        pl.len().alias('volume'),
        pl.sum('price').alias('total_ca')
    ]).to_pandas()
    
    fig_scatter = px.scatter(cat_analysis, x='volume', y='total_ca', size='avg_price', hover_name='category', color='total_ca', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_scatter, use_container_width=True)


# --- ONGLET 3 : SIMULATEUR ---
with tab3:
    st.subheader("Simulateur de Chiffre d'Affaires")
    st.write("Ajustez les paramètres pour voir l'impact immédiat sur les revenus de la plateforme.")
    
    c1, c2 = st.columns(2)
    with c1:
        price_adj = st.slider("Augmentation Prix de vente (%)", -20, 50, 0)
    with c2:
        volume_adj = st.slider("Augmentation Volume des ventes (%)", -20, 50, 0)
        
    # Simulation
    price_multiplier = 1 + (price_adj / 100)
    volume_multiplier = 1 + (volume_adj / 100)
    
    # Calculs simulés
    simulated_ca = ca_total * price_multiplier * volume_multiplier
    diff_ca = simulated_ca - ca_total
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Nouveau CA Total Estimé", f"${simulated_ca:,.2f}", f"{diff_ca:,.2f} $", delta_color="normal")
        
    with col_b:
        # Mini graphique de comparaison
        fig_comp = go.Figure(data=[
            go.Bar(name='CA Actuel', x=['Chiffre d\'Affaires'], y=[ca_total], marker_color='grey'),
            go.Bar(name='CA Simulé', x=['Chiffre d\'Affaires'], y=[simulated_ca], marker_color='#2ecc71' if diff_ca > 0 else '#e74c3c')
        ])
        fig_comp.update_layout(barmode='group')
        st.plotly_chart(fig_comp, use_container_width=True)
