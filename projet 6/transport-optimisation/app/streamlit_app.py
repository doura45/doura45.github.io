import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Optimisation des Coûts de Transport — Simulateur de Scénarios",
    layout="wide"
)

# --- CACHE DATA ---
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "SCMS_Delivery_History_Dataset.csv")
    
    df = pd.read_csv(DATA_PATH)
    
    df['Weight (Kilograms)'] = pd.to_numeric(df['Weight (Kilograms)'].replace('Weight Captured Separately', np.nan), errors='coerce')
    df['Freight Cost (USD)'] = pd.to_numeric(df['Freight Cost (USD)'].replace('Freight Included in Commodity Cost', np.nan).replace('Invoiced Separately', np.nan), errors='coerce')
    
    df['Delivered to Client Date'] = pd.to_datetime(df['Delivered to Client Date'], errors='coerce')
    df['PO Sent to Vendor Date'] = pd.to_datetime(df['PO Sent to Vendor Date'], errors='coerce')
    df['Delay_Days'] = (df['Delivered to Client Date'] - df['PO Sent to Vendor Date']).dt.days
    
    df = df.dropna(subset=['Shipment Mode', 'Weight (Kilograms)', 'Freight Cost (USD)'])
    df['Cost_per_Kg'] = df['Freight Cost (USD)'] / df['Weight (Kilograms)']
    
    # Remplacer les délais aberrants
    df.loc[df['Delay_Days'] < 0, 'Delay_Days'] = np.nan
    
    return df

@st.cache_data
def compute_kpis(df):
    total_cost = df['Freight Cost (USD)'].sum()
    total_shipments = len(df)
    avg_cost = df['Freight Cost (USD)'].mean()
    
    mode_distribution = df['Shipment Mode'].value_counts().reset_index()
    mode_distribution.columns = ['Mode', 'Count']
    
    cost_by_mode = df.groupby('Shipment Mode')['Freight Cost (USD)'].mean().reset_index()
    
    return total_cost, avg_cost, mode_distribution, cost_by_mode

# --- SIDEBAR ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.markdown("""
    Supply Chain Manager.
    Simulateur de réduction des coûts de fret.
    """)
    st.divider()

st.title("Optimisation des Coûts de Transport — Simulateur de Scénarios")
st.markdown("---")

df = load_data()
total_cost, avg_cost, mode_distribution, cost_by_mode = compute_kpis(df)

tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyse des Coûts", "Simulateur de Scénarios"])

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    col1, col2 = st.columns(2)
    col1.metric("Coût Total des Expéditions", f"${total_cost:,.0f}")
    col2.metric("Coût Moyen par Expédition", f"${avg_cost:,.0f}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Répartition des Modes de Transport")
        fig1 = px.pie(mode_distribution, values='Count', names='Mode', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.subheader("Coût Moyen par Mode de Transport")
        fig2 = px.bar(cost_by_mode, x='Shipment Mode', y='Freight Cost (USD)', color='Shipment Mode', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig2, use_container_width=True)

# --- ONGLET 2 : ANALYSE DES COÛTS ---
with tab2:
    modes_dispo = df['Shipment Mode'].unique().tolist()
    modes_dispo.insert(0, "Tous")
    selected_mode = st.selectbox("Filtrer par Mode de Transport :", modes_dispo)
    
    df_filtered = df if selected_mode == "Tous" else df[df['Shipment Mode'] == selected_mode]
    
    st.subheader("Relation Poids vs Coût")
    # Pour le graphique, retirer les extrêmes pour la lisibilité
    df_plot = df_filtered[df_filtered['Weight (Kilograms)'] < df_filtered['Weight (Kilograms)'].quantile(0.95)]
    fig_scatter = px.scatter(df_plot, x='Weight (Kilograms)', y='Freight Cost (USD)', color='Shipment Mode', opacity=0.6)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Routes (Pays) les plus coûteuses")
        top_routes = df_filtered.groupby('Country')['Freight Cost (USD)'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_routes = px.bar(top_routes, x='Freight Cost (USD)', y='Country', orientation='h', color='Freight Cost (USD)', color_continuous_scale='Reds')
        fig_routes.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_routes, use_container_width=True)
        
    with c2:
        st.subheader("Distribution des Délais (Jours)")
        fig_delay = px.box(df_filtered, x='Shipment Mode', y='Delay_Days', color='Shipment Mode')
        st.plotly_chart(fig_delay, use_container_width=True)

# --- ONGLET 3 : SIMULATEUR ---
with tab3:
    st.subheader("Simulateur d'Optimisation de la Supply Chain")
    st.write("Ajustez les leviers ci-dessous pour simuler un basculement de fret et estimer les économies immédiates.")
    
    # --- AFFICHAGE DES COÛTS RÉELS POUR LOGIQUE ---
    st.write("**Coûts Moyens réels par Expédition (Dataset) :**")
    cols_stats = st.columns(4)
    # Calculer les moyennes exactes pour l'affichage
    stats_mode = df.groupby('Shipment Mode')['Freight Cost (USD)'].mean()
    
    m_charter = stats_mode.get('Air Charter', 0)
    m_air = stats_mode.get('Air', 0)
    m_ocean = stats_mode.get('Ocean', 0)
    m_truck = stats_mode.get('Truck', 0)
    
    cols_stats[0].metric("Air Charter", f"${m_charter:,.0f}")
    cols_stats[1].metric("Air Standard", f"${m_air:,.0f}")
    cols_stats[2].metric("Ocean", f"${m_ocean:,.0f}")
    cols_stats[3].metric("Truck", f"${m_truck:,.0f}")
    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        charter_to_air = st.slider("Air Charter -> Air (%)", 0, 100, 20, help="Basculer du fret d'urgence vers du fret aérien standard.")
    with c2:
        ocean_to_truck = st.slider("Ocean -> Truck (%)", 0, 100, 0, help="Basculer du maritime vers le routier (si applicable).")
    with c3:
        weight_reduction = st.slider("Réduction de poids moyenne (%)", 0, 50, 0, help="Optimisation de l'emballage.")
        
    # Variables de base
    original_total = df['Freight Cost (USD)'].sum()
    
    # Dataframes par mode
    df_charter = df[df['Shipment Mode'] == 'Air Charter'].copy()
    df_air = df[df['Shipment Mode'] == 'Air'].copy()
    df_ocean = df[df['Shipment Mode'] == 'Ocean'].copy()
    df_truck = df[df['Shipment Mode'] == 'Truck'].copy()
    
    # --- CALCUL DES ÉCONOMIES (Logique Basée sur les Vrais Coûts) ---
    # 1. Économie Air Charter -> Air
    nb_charter = len(df_charter)
    economie_charter = nb_charter * (charter_to_air / 100) * (m_charter - m_air)
    
    # 2. Économie Ocean -> Truck
    nb_ocean = len(df_ocean)
    economie_ocean_truck = nb_ocean * (ocean_to_truck / 100) * (m_ocean - m_truck)
    
    # 3. Économie additionnelle via réduction de poids (emballage) sur le reste
    # On l'applique sur le coût total restant après conversions
    cout_restant = original_total - (nb_charter * (charter_to_air / 100) * m_charter) - (nb_ocean * (ocean_to_truck / 100) * m_ocean)
    economie_poids = cout_restant * (weight_reduction / 100)
    
    # 4. Totaux
    total_savings = economie_charter + economie_ocean_truck + economie_poids
    new_total_cost = original_total - total_savings
    
    # Impact délai (estimation)
    avg_delay_charter = df_charter['Delay_Days'].mean() if len(df_charter) > 0 else 0
    avg_delay_air = df_air['Delay_Days'].mean() if len(df_air) > 0 else 0
    
    avg_delay_ocean = df_ocean['Delay_Days'].mean() if len(df_ocean) > 0 else 0
    avg_delay_truck = df_truck['Delay_Days'].mean() if len(df_truck) > 0 else 0
    
    # Affichage Résultats
    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.metric("Coût Original", f"${original_total:,.0f}")
    res2.metric("Nouveau Coût Estimé", f"${new_total_cost:,.0f}")
    res3.metric("Économie Totale", f"${total_savings:,.0f}", delta=f"{total_savings:,.0f}", delta_color="normal")
    
    if charter_to_air > 0:
        st.info(f"💡 Info : Basculer {charter_to_air}% du Charter vers l'Air Standard réduit le coût unitaire de ${(m_charter-m_air):,.0f} sans impact majeur sur le délai.")
    if ocean_to_truck > 0:
        st.info(f"💡 Attention : Basculer {ocean_to_truck}% du Maritime vers le Routier change le délai moyen de **{avg_delay_ocean:.0f} jours à {avg_delay_truck:.0f} jours**.")
    
    # Graphique final
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Bar(x=['Avant Optimisation', 'Après Optimisation'], y=[original_total, new_total_cost], marker_color=['#e74c3c', '#2ecc71']))
    fig_sim.update_layout(title="Comparatif des Coûts", yaxis_title="Coût (USD)")
    st.plotly_chart(fig_sim, use_container_width=True)
