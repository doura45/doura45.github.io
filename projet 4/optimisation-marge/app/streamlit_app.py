import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Analyse Retail — Fofana Abdou",
    layout="wide"
)

# --- CHARGEMENT ET PRÉPARATION DES DONNÉES ---
@st.cache_data
def charger_et_preparer_donnees():
    # Définition des chemins vers les fichiers CSV
    dossier_actuel = os.path.dirname(__file__)
    chemin_data = os.path.join(dossier_actuel, "..", "data")
    
    # On charge les fichiers principaux du dataset Olist
    try:
        # Note : On utilise Pandas pour le chargement initial
        orders = pd.read_csv(os.path.join(chemin_data, "olist_orders_dataset.csv"))
        items = pd.read_csv(os.path.join(chemin_data, "olist_order_items_dataset.csv"))
        products = pd.read_csv(os.path.join(chemin_data, "olist_products_dataset.csv"))
        
        # --- UTILISATION DE DUCKDB POUR LES JOINTURES ---
        # C'est une méthode puissante pour manipuler des gros volumes avec du SQL
        requete_sql = """
        SELECT 
            i.order_id,
            o.order_purchase_timestamp AS date_achat,
            COALESCE(p.product_category_name, 'Autre') AS categorie,
            i.price AS prix_article
        FROM items i
        JOIN orders o ON i.order_id = o.order_id
        LEFT JOIN products p ON i.product_id = p.product_id
        WHERE o.order_status = 'delivered'
        """
        
        # On exécute la requête SQL et on transforme le résultat en DataFrame Pandas
        df_final = duckdb.query(requete_sql).df()
        
        # Conversion des dates pour les analyses temporelles
        df_final['date_achat'] = pd.to_datetime(df_final['date_achat'])
        df_final['mois_annee'] = df_final['date_achat'].dt.to_period('M').astype(str)
        
        return df_final
    except Exception as e:
        st.error(f"Erreur de lecture des données : {e}")
        return pd.DataFrame()

# Chargement effectif
df = charger_et_preparer_donnees()

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.write("Data Analyst Retail")
    st.markdown("---")
    st.info("Analyse de la performance commerciale basée sur le dataset public Olist (Brésil).")

# --- TITRE PRINCIPAL ---
st.title("Performance Commerciale — Olist Store")
st.markdown("---")

# Si les données sont vides, on arrête
if df.empty:
    st.warning("Les données n'ont pas pu être chargées.")
    st.stop()

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyse Catégories", "Simulateur de Croissance"])

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    # Indicateurs clés (KPIs)
    col1, col2, col3 = st.columns(3)
    
    ca_total = df['prix_article'].sum()
    nb_commandes = df['order_id'].nunique()
    panier_moyen = ca_total / nb_commandes
    
    col1.metric("Chiffre d'Affaires Total", f"{ca_total:,.0f} $")
    col2.metric("Total Commandes", f"{nb_commandes:,}")
    col3.metric("Panier Moyen", f"{panier_moyen:.2f} $")

    st.markdown("### Évolution Mensuelle du Chiffre d'Affaires")
    # Groupement par mois
    evolution = df.groupby('mois_annee')['prix_article'].sum().reset_index()
    
    fig_line = px.line(evolution, x='mois_annee', y='prix_article', 
                      title="Croissance du CA (Mensuel)",
                      markers=True, labels={'prix_article': 'CA ($)', 'mois_annee': 'Mois'})
    st.plotly_chart(fig_line, use_container_width=True)

# --- ONGLET 2 : ANALYSE DES CATÉGORIES ---
with tab2:
    st.subheader("Quelles sont les catégories les plus rentables ?")
    
    # Top 10 des catégories par CA
    top_categories = df.groupby('categorie')['prix_article'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig_bar = px.bar(top_categories, x='prix_article', y='categorie', 
                    orientation='h', color='prix_article',
                    title="Top 10 Catégories par Chiffre d'Affaires",
                    color_continuous_scale='Viridis',
                    labels={'prix_article': 'CA Total ($)', 'categorie': 'Catégorie'})
    st.plotly_chart(fig_bar, use_container_width=True)

# --- ONGLET 3 : SIMULATEUR DE CROISSANCE ---
with tab3:
    st.subheader("Simulateur d'Objectifs")
    st.write("Ajustez les leviers pour estimer l'impact sur le CA global :")
    
    c1, c2 = st.columns(2)
    with c1:
        hausse_prix = st.slider("Ajustement des Prix (%)", -20, 50, 0)
    with c2:
        hausse_volume = st.slider("Ajustement du Volume de ventes (%)", -20, 50, 0)
        
    # Calculs de simulation simples
    ca_actuel = ca_total
    ca_simule = ca_actuel * (1 + hausse_prix/100) * (1 + hausse_volume/100)
    difference_ca = ca_simule - ca_actuel
    
    st.markdown("---")
    st.metric("Chiffre d'Affaires Estimé", f"{ca_simule:,.0f} $", 
             delta=f"{difference_ca:,.0f} $", delta_color="normal")
    
    # Graphique de comparaison
    data_comp = pd.DataFrame({
        'Scénario': ['Actuel', 'Simulé'],
        'CA': [ca_actuel, ca_simule]
    })
    
    fig_comp = px.bar(data_comp, x='Scénario', y='CA', color='Scénario',
                     color_discrete_map={'Actuel': '#bdc3c7', 'Simulé': '#2ecc71'})
    st.plotly_chart(fig_comp, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Analyse réalisée par Fofana Abdou — Source : Dataset Olist")
