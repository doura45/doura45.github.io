import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Optimisation Transport — Fofana Abdou",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def charger_donnees():
    # On définit le chemin vers le fichier de données
    dossier_actuel = os.path.dirname(__file__)
    chemin_fichier = os.path.join(dossier_actuel, "..", "data", "SCMS_Delivery_History_Dataset.csv")
    
    # Lecture du fichier CSV
    df = pd.read_csv(chemin_fichier)
    
    # --- NETTOYAGE DES DONNÉES (Étape par étape) ---
    
    # 1. Nettoyage de la colonne Poids (Weight)
    # On remplace les textes d'erreur par du vide (NaN)
    df['Weight (Kilograms)'] = df['Weight (Kilograms)'].replace('Weight Captured Separately', np.nan)
    # On convertit en nombre
    df['Weight (Kilograms)'] = pd.to_numeric(df['Weight (Kilograms)'], errors='coerce')
    
    # 2. Nettoyage de la colonne Coût (Freight Cost)
    # On remplace les différentes mentions textuelles par du vide
    df['Freight Cost (USD)'] = df['Freight Cost (USD)'].replace('Freight Included in Commodity Cost', np.nan)
    df['Freight Cost (USD)'] = df['Freight Cost (USD)'].replace('Invoiced Separately', np.nan)
    # On convertit en nombre
    df['Freight Cost (USD)'] = pd.to_numeric(df['Freight Cost (USD)'], errors='coerce')
    
    # 3. Calcul des délais de livraison
    # Conversion des colonnes en format Date
    df['Delivered to Client Date'] = pd.to_datetime(df['Delivered to Client Date'], errors='coerce')
    df['PO Sent to Vendor Date'] = pd.to_datetime(df['PO Sent to Vendor Date'], errors='coerce')
    # Calcul de la différence en jours
    df['Delai_Livraison'] = (df['Delivered to Client Date'] - df['PO Sent to Vendor Date']).dt.days
    
    # 4. Suppression des lignes vides pour l'analyse
    df = df.dropna(subset=['Shipment Mode', 'Weight (Kilograms)', 'Freight Cost (USD)'])
    
    return df

# Exécution de la fonction de chargement
df = charger_donnees()

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.write("Analyste Supply Chain")
    st.markdown("---")
    st.write("Ce simulateur permet d'identifier des opportunités de réduction de coûts de fret.")

# --- TITRE PRINCIPAL ---
st.title("Optimisation des Coûts de Transport")
st.markdown("---")

# --- ONGLETS ---
onglet1, onglet2, onglet3 = st.tabs(["Vue Globale", "Analyse de la Dépense", "Simulateur d'Optimisation"])

# --- ONGLET 1 : VUE GLOBALE ---
with onglet1:
    col1, col2 = st.columns(2)
    
    # Calcul des indicateurs clés (KPIs)
    depense_totale = df['Freight Cost (USD)'].sum()
    cout_moyen_envoi = df['Freight Cost (USD)'].mean()
    
    col1.metric("Dépense Totale Fret", f"${depense_totale:,.0f}")
    col2.metric("Coût Moyen par Expédition", f"${cout_moyen_envoi:,.0f}")
    
    # --- SECTION GAIN POTENTIEL (Ajoutée par mes soins) ---
    st.markdown("---")
    st.subheader("Gain Potentiel d'Optimisation")
    
    # J'estime un gain conservateur de 12% basé sur l'analyse des modes
    taux_optimisation = 0.12
    gain_estime = depense_totale * taux_optimisation
    
    col_g1, col_g2 = st.columns([1, 2])
    col_g1.metric("Économie Possible", f"${gain_estime:,.0f}", delta="-12%")
    col_g2.write(f"""
    **Mon analyse :** En optimisant le mix transport (réduction de l'Air Charter au profit de l'Air Standard) 
    et en améliorant le conditionnement pour réduire le poids facturé, j'estime que nous pouvons économiser 
    environ **${gain_estime:,.0f}** sur le budget annuel.
    """)
    st.markdown("---")
    
    st.markdown("### Répartition du transport")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("**Modes de transport les plus utilisés**")
        repartition_modes = df['Shipment Mode'].value_counts().reset_index()
        fig1 = px.pie(repartition_modes, values='count', names='Shipment Mode', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.write("**Coût moyen par mode de transport**")
        cout_par_mode = df.groupby('Shipment Mode')['Freight Cost (USD)'].mean().reset_index()
        fig2 = px.bar(cout_par_mode, x='Shipment Mode', y='Freight Cost (USD)', 
                     color='Shipment Mode', labels={'Freight Cost (USD)': 'Coût Moyen ($)'})
        st.plotly_chart(fig2, use_container_width=True)

# --- ONGLET 2 : ANALYSE DE LA DÉPENSE ---
with onglet2:
    st.subheader("Analyse Corrélation Poids vs Prix")
    
    # Pour que le graphique soit lisible, on retire les colis extrêmement lourds (> 10 tonnes)
    df_filtre_poids = df[df['Weight (Kilograms)'] < 10000]
    
    fig3 = px.scatter(df_filtre_poids, x='Weight (Kilograms)', y='Freight Cost (USD)', 
                     color='Shipment Mode', opacity=0.4, 
                     title="Relation entre le poids du colis et le prix payé")
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info("On remarque que le transport Aérien (Air) est souvent utilisé même pour des poids élevés, ce qui augmente les coûts.")

# --- ONGLET 3 : SIMULATEUR D'OPTIMISATION ---
with onglet3:
    st.subheader("Simulateur d'économies potentielles")
    st.write("Ajustez les curseurs pour voir l'impact sur le budget annuel :")
    
    # Récupération des prix moyens réels pour la simulation
    couts_moyens = df.groupby('Shipment Mode')['Freight Cost (USD)'].mean()
    prix_moyen_charter = couts_moyens.get('Air Charter', 0)
    prix_moyen_air_std = couts_moyens.get('Air', 0)
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        st.write("**Levier 1 : Basculement Modal**")
        transfert = st.slider("% de vols 'Charter' à passer en 'Air Standard'", 0, 100, 20)
        st.caption("L'Air Charter est très coûteux par rapport à l'Air classique.")
        
    with col_sim2:
        st.write("**Levier 2 : Optimisation Emballage**")
        gain_poids = st.slider("% de réduction de poids (optimisation colis)", 0, 30, 0)
    
    # --- CALCULS DE LA SIMULATION ---
    
    # 1. Économie sur le basculement Charter -> Air
    nb_envois_charter = len(df[df['Shipment Mode'] == 'Air Charter'])
    gain_par_envoi = prix_moyen_charter - prix_moyen_air_std
    economie_mode = nb_envois_charter * (transfert / 100) * gain_par_envoi
    
    # 2. Économie sur la réduction de poids globale
    budget_actuel = df['Freight Cost (USD)'].sum()
    # Calcul de l'économie sur le poids (Hypothèse plus réaliste : Gain de 0.5% en coût pour 1% de poids gagné)
    gain_poids_reel = (gain_poids / 100) * budget_actuel * 0.5
    
    # 3. Résultats finaux
    economie_totale = economie_mode + gain_poids_reel
    nouveau_budget = budget_actuel - economie_totale
    
    st.markdown("---")
    res_a, res_b = st.columns(2)
    
    res_a.metric("Économie Estimée", f"${economie_totale:,.0f}", delta=f"{economie_totale:,.0f}")
    res_b.metric("Nouveau Budget Prévisionnel", f"${nouveau_budget:,.0f}")
    
    # Graphique de comparaison Avant / Après
    comparaison = pd.DataFrame({
        'Situation': ['Avant Optimisation', 'Après Optimisation'],
        'Coût Total': [budget_actuel, nouveau_budget]
    })
    
    fig_bilan = px.bar(comparaison, x='Situation', y='Coût Total', 
                      color='Situation', color_discrete_map={'Avant Optimisation': '#e74c3c', 'Après Optimisation': '#2ecc71'})
    st.plotly_chart(fig_bilan, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Développé par Fofana Abdou — Data Analyst Supply Chain & Finance")
