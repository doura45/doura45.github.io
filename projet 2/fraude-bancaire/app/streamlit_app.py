import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
import shap

# Détection de Fraude Bancaire — Analyse des Transactions

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Détection de Fraude Bancaire — Analyse des Transactions",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ET DU MODÈLE ---
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "creditcard.csv")
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
    **Détection de Fraude Bancaire**
    J'ai développé ce système pour identifier les transactions frauduleuses parmi des milliers de paiements légitimes, en utilisant un modèle Random Forest optimisé.
    """)
    st.divider()
    st.info("Utilisez les onglets pour explorer les données et tester le simulateur.")

# --- TITRE PRINCIPAL ---
st.title("Détection de Fraude Bancaire — Analyse des Transactions")
st.markdown("---")

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["Vue Globale", "Analyse des Fraudes", "Simulateur de Transaction"])

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    col1, col2, col3 = st.columns(3)
    
    fraud_rate = (df['Class'].value_counts(normalize=True)[1] * 100)
    col1.metric("Taux de Fraude", f"{fraud_rate:.4f}%")
    col2.metric("Total Transactions", f"{len(df):,}")
    col3.metric("Nombre de Fraudes", f"{df['Class'].sum()}")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Déséquilibre des classes")
        fig_count = px.bar(df['Class'].value_counts().reset_index(), 
                           x='Class', y='count', color='Class',
                           log_y=True, labels={'count': 'Nombre (Log)', 'Class': '0: Normal, 1: Fraude'},
                           color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig_count, use_container_width=True)
        
    with c2:
        st.subheader("Distribution des Montants")
        fig_dist = px.box(df, x='Class', y='Amount', color='Class',
                          log_y=True, labels={'Amount': 'Montant (Log)', 'Class': 'Type'},
                          color_discrete_map={0: '#2ecc71', 1: '#e74c3c'})
        st.plotly_chart(fig_dist, use_container_width=True)

# --- ONGLET 2 : ANALYSE DES FRAUDES ---
with tab2:
    st.subheader("Comprendre les décisions du modèle")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Top 10 Variables Importantes**")
        importances = pd.Series(model.feature_importances_, index=model_columns)
        top_10 = importances.nlargest(10).reset_index()
        top_10.columns = ['Variable', 'Importance']
        fig_imp = px.bar(top_10, x='Importance', y='Variable', orientation='h',
                         color='Importance', color_continuous_scale='Reds')
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with col_b:
        st.write("**Heures les plus fréquentes pour la fraude**")
        # On convertit le temps (secondes) en heures (0-23)
        df['Hour'] = (df['Time'] / 3600) % 24
        fraud_hours = df[df['Class'] == 1]['Hour']
        fig_hour = px.histogram(fraud_hours, nbins=24, 
                                labels={'value': 'Heure de la journée'},
                                color_discrete_sequence=['#e74c3c'])
        st.plotly_chart(fig_hour, use_container_width=True)

    st.divider()
    st.write("**Graphique SHAP (Explication globale)**")
    # Pour Streamlit, on utilise un échantillon et on affiche via matplotlib
    import matplotlib.pyplot as plt
    X_sample = df.drop('Class', axis=1).sample(100, random_state=42)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    fig_shap, ax_shap = plt.subplots()
    if isinstance(shap_values, list):
        shap.summary_plot(shap_values[1], X_sample, plot_type='dot', show=False)
    else:
        shap.summary_plot(shap_values, X_sample, plot_type='dot', show=False)
    st.pyplot(fig_shap)

# --- ONGLET 3 : SIMULATEUR DE TRANSACTION ---
with tab3:
    st.subheader("Analyser une nouvelle transaction")
    
    # Récupération des 5 variables les plus importantes
    top_5_features = importances.nlargest(5).index.tolist()
    
    with st.form("sim_form"):
        c1, c2 = st.columns(2)
        with c1:
            amount = st.slider("Montant de la transaction ($)", 0, 5000, 100)
            hour = st.slider("Heure de la transaction (0-23h)", 0, 23, 12)
        
        with c2:
            v_vals = {}
            for v in top_5_features:
                if v not in ['Amount', 'Time']:
                    v_vals[v] = st.slider(f"Variable {v}", -5.0, 5.0, 0.0)
            
        submit = st.form_submit_button("Analyser la transaction")
        
        if submit:
            # Préparation de l'entrée
            input_dict = {col: 0 for col in model_columns}
            input_dict['Amount'] = amount
            input_dict['Time'] = hour * 3600 # Conversion grossière
            for v, val in v_vals.items():
                input_dict[v] = val
            
            input_df = pd.DataFrame([input_dict])
            prob = model.predict_proba(input_df)[0][1]
            
            st.divider()
            
            # Jauge de risque
            if prob < 0.2:
                st.success(f"### Résultat : Transaction Légitime ✅")
                color = "green"
            elif prob < 0.6:
                st.warning(f"### Résultat : Transaction Suspecte ⚠️")
                color = "orange"
            else:
                st.error(f"### Résultat : Transaction Frauduleuse 🚨")
                color = "red"
            
            st.write(f"Probabilité de fraude : **{prob*100:.1f}%**")
            
            # Affichage visuel de la jauge
            st.markdown(f"""
            <div style="background-color: lightgrey; width: 100%; border-radius: 10px;">
                <div style="background-color: {color}; width: {prob*100}%; height: 20px; border-radius: 10px;"></div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Étude et développement réalisés par fofana abdou - 2026")
