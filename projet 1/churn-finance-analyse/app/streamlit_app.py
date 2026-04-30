import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Analyse du Churn Client",
    layout="wide"
)

# --- CHARGEMENT DES FICHIERS ---
# On définit où se trouvent nos fichiers de manière explicite
dossier_actuel = os.path.dirname(__file__)
chemin_data = os.path.join(dossier_actuel, "..", "data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
chemin_modele = os.path.join(dossier_actuel, "model.joblib")
chemin_colonnes = os.path.join(dossier_actuel, "model_columns.joblib")

@st.cache_data
def charger_donnees():
    # Chargement du CSV
    df = pd.read_csv(chemin_data)
    
    # Nettoyage de la colonne TotalCharges (étape par étape)
    # 1. On force la conversion en nombre, les erreurs (cases vides) deviennent des "NaN"
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    # 2. On remplace les cases vides (NaN) par 0 pour pouvoir faire des calculs
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    return df

@st.cache_resource
def charger_modele():
    # Chargement du modèle de Machine Learning et des colonnes nécessaires
    model = joblib.load(chemin_modele)
    colonnes = joblib.load(chemin_colonnes)
    return model, colonnes

# Exécution du chargement avec une sécurité
try:
    df = charger_donnees()
    model, model_columns = charger_modele()
except Exception as e:
    st.error(f"Erreur lors du chargement des fichiers : {e}")
    st.stop()

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.write("Data Analyst")
    st.markdown("---")
    st.info("Utilisez les onglets pour explorer l'analyse.")

# --- TITRE PRINCIPAL ---
st.title("Analyse du Churn — Secteur Télécom")
st.markdown("---")

# --- ONGLETS ---
onglet1, onglet2, onglet3 = st.tabs(["Vue Globale", "Analyse des Causes", "Simulateur de Risque"])

# --- ONGLET 1 : VUE GLOBALE ---
with onglet1:
    col_m1, col_m2, col_m3 = st.columns(3)
    
    # Calculs simples pour les métriques
    total_clients = len(df)
    clients_partis = len(df[df['Churn'] == 'Yes'])
    taux_de_churn = (clients_partis / total_clients) * 100
    panier_moyen = df['MonthlyCharges'].mean()

    col_m1.metric("Taux de Churn", f"{taux_de_churn:.1f}%")
    col_m2.metric("Total Clients", total_clients)
    col_m3.metric("Revenu Moyen Mensuel", f"${panier_moyen:.2f}")

    st.markdown("### Répartition des clients")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("**Départs vs Fidèles**")
        fig_pie = px.pie(df, names='Churn', hole=0.5, 
                         color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.write("**Taux de départ par type de contrat**")
        # On calcule le taux de départ pour chaque contrat
        df_contrat = df.groupby('Contract')['Churn'].value_counts(normalize=True).unstack()
        df_contrat = df_contrat.reset_index()
        
        fig_bar = px.bar(df_contrat, x='Contract', y='Yes', 
                         title="Probabilité de départ par contrat",
                         labels={'Yes': 'Taux de Churn (%)'},
                         color='Contract')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- ONGLET 2 : ANALYSE DES CAUSES ---
with onglet2:
    st.subheader("Facteurs influençant le départ")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Impact du prix (Monthly Charges)**")
        fig_box = px.box(df, x="Churn", y="MonthlyCharges", color="Churn",
                         color_discrete_map={'No': '#2ecc71', 'Yes': '#e74c3c'})
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_b:
        st.write("**Impact de l'ancienneté (Tenure)**")
        # On regarde l'ancienneté moyenne
        anciennete_moyenne = df.groupby('Churn')['tenure'].mean().reset_index()
        fig_tenure = px.bar(anciennete_moyenne, x='Churn', y='tenure', color='Churn',
                            labels={'tenure': 'Moyenne de mois de présence'})
        st.plotly_chart(fig_tenure, use_container_width=True)

# --- ONGLET 3 : SIMULATEUR DE RISQUE ---
with onglet3:
    st.subheader("Prédire le risque pour un nouveau client")
    st.write("Le modèle Random Forest identifie les clients à risque avec une précision globale de 80%.")
    st.info("Note technique : Pour maximiser la détection (Recall à 70.1%), le seuil de probabilité a été optimisé à 0.3.")
    
    with st.form("simulateur"):
        col1, col2 = st.columns(2)
        
        with col1:
            tenure_input = st.slider("Ancienneté (nombre de mois)", 0, 72, 12)
            contract_input = st.selectbox("Type de contrat", ["Month-to-month", "One year", "Two year"])
        
        with col2:
            charges_input = st.number_input("Montant de la facture mensuelle ($)", 20, 150, 70)
            internet_input = st.selectbox("Service Internet", ["Fiber optic", "DSL", "No"])
            
        bouton_calcul = st.form_submit_button("Estimer le risque")
        
        if bouton_calcul:
            # --- PRÉPARATION DES DONNÉES (Méthode explicite) ---
            # On crée un dictionnaire avec toutes les colonnes du modèle mises à 0
            nouveau_client = {}
            for col in model_columns:
                nouveau_client[col] = 0
            
            # On remplit les valeurs saisies
            nouveau_client['tenure'] = tenure_input
            nouveau_client['MonthlyCharges'] = charges_input
            
            # On gère le One-Hot Encoding (manuellement pour être clair)
            colonne_contrat = "Contract_" + contract_input
            if colonne_contrat in nouveau_client:
                nouveau_client[colonne_contrat] = 1
                
            colonne_internet = "InternetService_" + internet_input
            if colonne_internet in nouveau_client:
                nouveau_client[colonne_internet] = 1
            
            # Conversion en DataFrame pour le modèle
            df_prediction = pd.DataFrame([nouveau_client])
            
            # Calcul de la probabilité
            proba = model.predict_proba(df_prediction)[0][1]
            risque_pourcentage = proba * 100
            
            st.markdown("---")
            if proba > 0.35:
                st.error(f"### Risque élevé : {risque_pourcentage:.1f}%")
                st.warning("Le client présente des caractéristiques typiques de départ.")
            else:
                st.success(f"### Risque faible : {risque_pourcentage:.1f}%")
                st.info("Le client est probablement fidèle.")
            
            st.progress(proba)

# --- FOOTER ---
st.markdown("---")
st.caption("Étude et développement réalisés par Fofana Abdou — Data Analyst Portfolio 2026")
