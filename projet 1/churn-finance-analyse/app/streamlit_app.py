import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CHEMINS ABSOLUS POUR ÉVITER LES ERREURS ---
# On récupère le dossier où se trouve ce script (le dossier 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Le dossier data est au même niveau que le dossier app
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
COLUMNS_PATH = os.path.join(BASE_DIR, "model_columns.joblib")

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Analyse du Churn Client",
    page_icon="🏦",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ET DU MODÈLE ---
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    columns = joblib.load(COLUMNS_PATH)
    return model, columns

# Chargement sécurisé
try:
    df = load_data()
    model, model_columns = load_model()
except Exception as e:
    st.error(f"Erreur de chargement des fichiers : {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Fofana Abdou")
    st.markdown("""
    **Étude de la Fidélisation Client**
    J'ai conçu cette plateforme pour visualiser les résultats de mes recherches sur le churn et tester les capacités prédictives de mon modèle en temps réel.
    """)
    st.divider()
    st.info("Utilisez les onglets pour naviguer entre les analyses.")

# --- TITRE PRINCIPAL ---
st.title("🏦 Analyse du Churn Client — Secteur Bancaire")
st.markdown("---")

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["Vue Globale", "Causes du Churn", "Simulateur Client"])

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    col1, col2, col3 = st.columns(3)
    
    # Métrique principale (calculée dynamiquement)
    real_churn_rate = (df['Churn'].value_counts(normalize=True)['Yes'] * 100)
    col1.metric("Taux de Churn Global", f"{real_churn_rate:.1f}%")
    col2.metric("Total Clients", f"{len(df)}")
    col3.metric("Revenu Moyen (Mensuel)", f"${df['MonthlyCharges'].mean():.2f}")

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Répartition du Churn")
        fig_pie = px.pie(df, names='Churn', hole=0.5, 
                         color_discrete_sequence=['#2ecc71', '#e74c3c'],
                         labels={'Churn': 'Départ'})
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_right:
        st.subheader("Taux de Churn par Type de Contrat")
        # Calcul du taux par contrat
        contract_churn = df.groupby('Contract')['Churn'].value_counts(normalize=True).unstack()['Yes'] * 100
        contract_churn = contract_churn.reset_index()
        contract_churn.columns = ['Type de Contrat', 'Taux de Churn (%)']
        
        fig_bar = px.bar(contract_churn, 
                         x='Type de Contrat', 
                         y='Taux de Churn (%)',
                         color='Type de Contrat',
                         text='Taux de Churn (%)',
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         labels={'Taux de Churn (%)': 'Taux (%)'})
        
        # Formatage des labels sur les barres
        fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- ONGLET 2 : CAUSES DU CHURN ---
with tab2:
    st.subheader("Analyse des comportements de départ")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Impact des Mensualités**")
        fig_box = px.box(df, x="Churn", y="MonthlyCharges", color="Churn",
                         color_discrete_map={'No': '#2ecc71', 'Yes': '#e74c3c'},
                         labels={'MonthlyCharges': 'Frais Mensuels ($)'})
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_b:
        st.write("**Impact de l'Ancienneté**")
        tenure_avg = df.groupby('Churn')['tenure'].mean().reset_index()
        fig_tenure = px.bar(tenure_avg, x='Churn', y='tenure', color='Churn',
                            color_discrete_map={'No': '#2ecc71', 'Yes': '#e74c3c'},
                            labels={'tenure': 'Ancienneté Moyenne (Mois)'})
        st.plotly_chart(fig_tenure, use_container_width=True)
        
    st.divider()
    
    # Top 5 Variables
    st.subheader("🎯 Les 5 facteurs déterminants de mon modèle")
    importances = pd.Series(model.feature_importances_, index=model_columns)
    top_5 = importances.nlargest(5).reset_index()
    top_5.columns = ['Variable', 'Importance']
    
    fig_imp = px.bar(top_5, x='Importance', y='Variable', orientation='h',
                     color='Importance', color_continuous_scale='Greens')
    st.plotly_chart(fig_imp, use_container_width=True)

# --- ONGLET 3 : SIMULATEUR CLIENT ---
with tab3:
    st.subheader("Estimation du risque pour un nouveau profil")
    
    with st.form("prediction_form"):
        c1, c2 = st.columns(2)
        
        with c1:
            tenure = st.slider("Ancienneté (mois)", 0, 72, 12)
            contract = st.selectbox("Type de contrat", ["Month-to-month", "One year", "Two year"])
            internet = st.selectbox("Service Internet", ["Fiber optic", "DSL", "No"])
            
        with c2:
            monthly = st.slider("Mensualité ($)", 20, 120, 70)
            tech_support = st.selectbox("Support Technique", ["No", "Yes", "No internet service"])
            
        submit = st.form_submit_button("Calculer le risque de départ")
        
        if submit:
            input_dict = {col: 0 for col in model_columns}
            input_dict['tenure'] = tenure
            input_dict['MonthlyCharges'] = monthly
            
            if f'Contract_{contract}' in input_dict: input_dict[f'Contract_{contract}'] = 1
            if f'InternetService_{internet}' in input_dict: input_dict[f'InternetService_{internet}'] = 1
            if f'TechSupport_{tech_support}' in input_dict: input_dict[f'TechSupport_{tech_support}'] = 1
            
            input_df = pd.DataFrame([input_dict])
            prob = model.predict_proba(input_df)[0][1]
            prediction = "DÉPART" if prob > 0.3 else "FIDÈLE"
            
            st.divider()
            if prediction == "DÉPART":
                st.error(f"### Résultat : Ce client risque de partir 🚨")
                st.warning(f"Probabilité de churn : **{prob*100:.1f}%**")
            else:
                st.success(f"### Résultat : Ce client est probablement fidèle ✅")
                st.info(f"Probabilité de churn : **{prob*100:.1f}%**")
            
            st.progress(prob)

# --- FOOTER ---
st.markdown("---")
st.caption("Étude et développement réalisés par fofana abdou - 2026")
