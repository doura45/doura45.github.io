import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Scoring de Crédit — Fofana Abdou",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ET DU MODÈLE ---
@st.cache_data
def charger_donnees():
    # On définit le chemin vers le fichier de données
    dossier_actuel = os.path.dirname(__file__)
    chemin_data = os.path.join(dossier_actuel, "..", "data", "application_train.csv")
    # Chargement du dataset
    df = pd.read_csv(chemin_data)
    return df

@st.cache_resource
def charger_modele():
    dossier_actuel = os.path.dirname(__file__)
    # Chargement du modèle de scoring et des noms de colonnes
    model = joblib.load(os.path.join(dossier_actuel, "model.joblib"))
    columns = joblib.load(os.path.join(dossier_actuel, "model_columns.joblib"))
    return model, columns

# Exécution du chargement
try:
    df = charger_donnees()
    model, model_columns = charger_modele()
except Exception as e:
    st.error(f"Erreur lors du chargement des fichiers : {e}")
    st.stop()

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.write("Analyste de Risque")
    st.markdown("---")
    st.write("Ce simulateur évalue la probabilité de défaut de paiement pour une demande de crédit bancaire.")

# --- TITRE PRINCIPAL ---
st.title("Scoring de Crédit — Risque Bancaire")
st.markdown("---")

# --- ONGLETS ---
onglet1, onglet2, onglet3 = st.tabs(["Panorama des Crédits", "Analyse du Risque", "Simulateur de Crédit"])

# --- ONGLET 1 : PANORAMA DES CRÉDITS ---
with onglet1:
    col_x, col_y, col_z = st.columns(3)
    
    nb_dossiers = len(df)
    # Dans ce dataset, TARGET = 1 signifie un défaut de paiement
    taux_defaut_global = df['TARGET'].mean() * 100
    revenu_moyen_annuel = df['AMT_INCOME_TOTAL'].mean()
    
    col_x.metric("Dossiers Analysés", f"{nb_dossiers:,}")
    col_y.metric("Taux de Défaut Global", f"{taux_defaut_global:.2f}%")
    col_z.metric("Revenu Moyen Annuel", f"${revenu_moyen_annuel:,.0f}")

    st.markdown("### Distribution des montants de crédits")
    # Histogramme simple pour voir la répartition des prêts
    fig1 = px.histogram(df, x='AMT_CREDIT', nbins=50, 
                       title="Répartition des montants de crédits accordés",
                       color_discrete_sequence=['#3498db'])
    st.plotly_chart(fig1, use_container_width=True)

# --- ONGLET 2 : ANALYSE DU RISQUE ---
with onglet2:
    st.subheader("Quels facteurs causent le défaut de paiement ?")
    st.write("Voici les variables qui influencent le plus la décision du modèle de scoring :")
    
    # On récupère l'importance des variables (Feature Importance)
    importances = pd.Series(model.feature_importances_, index=model_columns)
    top_10_variables = importances.nlargest(10).reset_index()
    top_10_variables.columns = ['Variable', 'Importance']
    
    fig2 = px.bar(top_10_variables, x='Importance', y='Variable', orientation='h',
                 color='Importance', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("L'ancienneté professionnelle, l'âge et les sources de données externes sont les indicateurs de risque majeurs.")

# --- ONGLET 3 : SIMULATEUR DE CRÉDIT ---
with onglet3:
    st.subheader("Évaluer un nouveau dossier client")
    st.write("Saisissez les informations du client pour obtenir une recommandation :")
    
    with st.form("form_scoring"):
        c1, c2 = st.columns(2)
        
        with c1:
            montant_pret = st.number_input("Montant du crédit souhaité ($)", 5000, 1000000, 50000)
            revenu_client = st.number_input("Revenu annuel du client ($)", 5000, 500000, 30000)
        
        with c2:
            age_client = st.slider("Âge du client", 18, 80, 30)
            type_pret = st.selectbox("Type de contrat", ["Cash loans", "Revolving loans"])
            
        bouton_eval = st.form_submit_button("Évaluer le dossier")
        
        if bouton_eval:
            # --- PRÉPARATION DU PROFIL (Méthode explicite) ---
            profil_client = {}
            for col in model_columns:
                profil_client[col] = 0 # On initialise tout à 0
            
            # On remplit les données saisies
            profil_client['AMT_CREDIT'] = montant_pret
            profil_client['AMT_INCOME_TOTAL'] = revenu_client
            # Le modèle a été entraîné avec l'âge en jours (négatif)
            profil_client['DAYS_BIRTH'] = -age_client * 365
            
            # Gestion du type de contrat (One-Hot Encoding manuel)
            nom_col_contrat = "NAME_CONTRACT_TYPE_" + type_pret
            if nom_col_contrat in profil_client:
                profil_client[nom_col_contrat] = 1
            
            # Conversion en DataFrame
            df_simulation = pd.DataFrame([profil_client])
            
            # Calcul de la probabilité de défaut
            proba_defaut = model.predict_proba(df_simulation)[0][1]
            pourcentage_risque = proba_defaut * 100
            
            st.markdown("---")
            st.write(f"Probabilité de défaut estimée : **{pourcentage_risque:.1f}%**")
            st.progress(proba_defaut)
            
            if proba_defaut < 0.35:
                st.success("### AVIS FAVORABLE")
                st.write("Le risque est jugé acceptable pour l'octroi du crédit.")
            elif proba_defaut < 0.60:
                st.warning("### DOSSIER À ÉTUDIER")
                st.write("Le profil présente des risques modérés. Des garanties supplémentaires peuvent être requises.")
            else:
                st.error("### AVIS DÉFAVORABLE")
                st.write("Le risque de défaut est trop élevé pour ce profil.")

# --- FOOTER ---
st.markdown("---")
st.caption("Développé par Fofana Abdou — Data Analyst Risk Management")
