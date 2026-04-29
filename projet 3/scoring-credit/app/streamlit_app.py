import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Scoring de Crédit — Évaluation du Risque Bancaire",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ET DU MODÈLE ---
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "application_train.csv")
    # Chargement du dataset (déjà échantillonné à ~49000 lignes)
    df = pd.read_csv(DATA_PATH)
    return df

@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model = joblib.load(os.path.join(BASE_DIR, "model.joblib"))
    columns = joblib.load(os.path.join(BASE_DIR, "model_columns.joblib"))
    return model, columns

try:
    df = load_data()
    model, model_columns = load_model()
except Exception as e:
    st.error(f"Erreur de chargement : {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.markdown("""
    Scoring de Crédit — Évaluation du Risque Bancaire.
    Analyse prédictive du risque de défaut de paiement pour les demandes de crédit.
    """)
    st.divider()

# --- TITRE PRINCIPAL ---
st.title("Scoring de Crédit — Évaluation du Risque Bancaire")
st.markdown("---")

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyse du Risque", "Simulateur Client"])

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    col1, col2, col3 = st.columns(3)
    
    taux_defaut = (df['TARGET'].mean() * 100)
    col1.metric("Taux de Défaut Global", f"{taux_defaut:.2f}%")
    col2.metric("Total Clients Analysés", f"{len(df):,}")
    col3.metric("Revenu Moyen Annuel", f"${df['AMT_INCOME_TOTAL'].mean():.0f}")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Déséquilibre des classes")
        fig_pie = px.pie(df, names='TARGET', hole=0.5, 
                         color_discrete_sequence=['#2ecc71', '#e74c3c'],
                         labels={'TARGET': 'Défaut'})
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Distribution des Revenus")
        fig_income = px.histogram(df[df['AMT_INCOME_TOTAL'] < 300000], x='AMT_INCOME_TOTAL', 
                                  nbins=30, color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig_income, use_container_width=True)

    st.subheader("Distribution du Montant des Crédits")
    fig_credit = px.histogram(df, x='AMT_CREDIT', nbins=50, color_discrete_sequence=['#9b59b6'])
    st.plotly_chart(fig_credit, use_container_width=True)

# --- ONGLET 2 : ANALYSE DU RISQUE ---
with tab2:
    st.subheader("Comprendre les décisions du modèle")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Top 10 Variables Importantes**")
        importances = pd.Series(model.feature_importances_, index=model_columns)
        top_10 = importances.nlargest(10).reset_index()
        top_10.columns = ['Variable', 'Importance']
        fig_imp = px.bar(top_10, x='Importance', y='Variable', orientation='h',
                         color='Importance', color_continuous_scale='Blues')
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with col_b:
        st.write("**Corrélation des variables avec le défaut**")
        # Calcul simplifié pour l'affichage
        corr = df.select_dtypes(include=['number']).corr()['TARGET'].sort_values()
        top_corr = pd.concat([corr.head(5), corr.tail(6)]).drop('TARGET', errors='ignore')
        fig_corr = px.bar(top_corr, orientation='h', color_discrete_sequence=['#e67e22'])
        st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()
    st.write("**Analyse de l'impact des variables (SHAP)**")
    st.info("Le graphique SHAP permet de voir comment chaque variable influence la probabilité finale.")
    # On affiche une image placeholder ou on explique qu'il est calculé sur demande
    st.image("https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/shap_diagram.png", width=400)

# --- ONGLET 3 : SIMULATEUR CLIENT ---
with tab3:
    st.subheader("Évaluation en temps réel pour un nouveau profil")
    
    with st.form("prediction_form"):
        c1, c2 = st.columns(2)
        
        with c1:
            amt_credit = st.slider("Montant du crédit ($)", 10000, 1000000, 100000)
            income = st.slider("Revenu annuel ($)", 10000, 500000, 50000)
            age = st.slider("Âge", 18, 70, 35)
            
        with c2:
            contract = st.selectbox("Type de contrat", ["Cash loans", "Revolving loans"])
            realty = st.selectbox("Propriétaire immobilier", ["Yes", "No"])
            prev_credits = st.slider("Nombre de crédits précédents", 0, 20, 2)
            
        submit = st.form_submit_button("Évaluer le risque de crédit")
        
        if submit:
            # Préparation d'une entrée bidon basée sur les colonnes du modèle
            input_dict = {col: 0 for col in model_columns}
            
            # Mapping des sliders
            input_dict['AMT_CREDIT'] = amt_credit
            input_dict['AMT_INCOME_TOTAL'] = income
            input_dict['DAYS_BIRTH'] = -age * 365
            input_dict['NB_PREV_CREDITS'] = prev_credits
            
            # Mapping des catégories (selon l'encodage One-Hot)
            if f'NAME_CONTRACT_TYPE_{contract}' in input_dict: input_dict[f'NAME_CONTRACT_TYPE_{contract}'] = 1
            if f'FLAG_OWN_REALTY_{"Y" if realty == "Yes" else "N"}' in input_dict: input_dict[f'FLAG_OWN_REALTY_{"Y" if realty == "Yes" else "N"}'] = 1
            
            input_df = pd.DataFrame([input_dict])
            prob = model.predict_proba(input_df)[0][1]
            
            st.divider()
            
            if prob < 0.3:
                st.success(f"### Résultat : Crédit Accordé ✅")
                status = "FIDÈLE"
                color = "green"
            elif prob < 0.6:
                st.warning(f"### Résultat : Risque Modéré ⚠️")
                status = "SUSPECT"
                color = "orange"
            else:
                st.error(f"### Résultat : Crédit Refusé 🚨")
                status = "RISQUE"
                color = "red"
            
            st.write(f"Probabilité de défaut : **{prob*100:.1f}%**")
            
            # Jauge visuelle
            st.markdown(f"""
            <div style="background-color: lightgrey; width: 100%; border-radius: 10px;">
                <div style="background-color: {color}; width: {prob*100}%; height: 20px; border-radius: 10px;"></div>
            </div>
            """, unsafe_allow_html=True)

st.caption("Étude et développement réalisés par fofana abdou - 2026")
