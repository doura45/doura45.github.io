import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Détection de Fraude — Fofana Abdou",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ET DU MODÈLE ---
@st.cache_data
def charger_donnees():
    # On définit le chemin vers le fichier CSV
    dossier_actuel = os.path.dirname(__file__)
    chemin_data = os.path.join(dossier_actuel, "..", "data", "creditcard.csv")
    df = pd.read_csv(chemin_data)
    return df

@st.cache_resource
def charger_modele():
    dossier_actuel = os.path.dirname(__file__)
    # Chargement du modèle de Machine Learning et des noms de colonnes
    model = joblib.load(os.path.join(dossier_actuel, "model.joblib"))
    columns = joblib.load(os.path.join(dossier_actuel, "model_columns.joblib"))
    return model, columns

# Exécution du chargement avec gestion d'erreur simple
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
    st.write("Ce projet utilise un modèle de Machine Learning pour identifier les transactions bancaires à risque.")

# --- TITRE PRINCIPAL ---
st.title("Détection de Fraude Bancaire")
st.markdown("---")

# --- ONGLETS ---
onglet1, onglet2, onglet3 = st.tabs(["Statistiques Globales", "Facteurs de Risque", "Testeur de Transaction"])

# --- ONGLET 1 : STATISTIQUES GLOBALES ---
with onglet1:
    col_a, col_b, col_c = st.columns(3)
    
    total_trans = len(df)
    nb_fraudes = df['Class'].sum()
    taux_fraude = (nb_fraudes / total_trans) * 100
    
    col_a.metric("Total Transactions", f"{total_trans:,}")
    col_b.metric("Nombre de Fraudes", nb_fraudes)
    col_c.metric("Taux de Fraude", f"{taux_fraude:.4f}%")

    # --- SECTION IMPACT FINANCIER (Ajoutée par mes soins) ---
    st.markdown("---")
    st.subheader("Impact Financier du Modèle")
    
    # Note : L'application utilise un échantillon de 50 000 transactions (Taux fraude local : 0.97%)
    # pour refléter la performance sur le dataset original (Taux fraude : 0.17%)
    montant_moyen_fraude = df[df['Class']==1]['Amount'].mean()
    fraudes_detectees = int(nb_fraudes * 0.7449) # Recall exact du modèle
    montant_sauvegarde = fraudes_detectees * montant_moyen_fraude
    
    st.write("J'ai analysé l'impact économique du modèle (Recall de 74.49%) :")
    
    st.markdown(f"""
    - **Taux de fraude original :** 0.17 %
    - **Fraudes détectées par le modèle :** {fraudes_detectees}
    - **Montant protégé estimé :** {montant_sauvegarde:,.2f} $
    """)
    st.markdown("---")

    st.markdown("### Répartition Normal vs Fraude")
    st.write("Note : On remarque que les transactions frauduleuses sont extrêmement rares (moins de 1%).")
    
    # Préparation des données pour le graphique
    df_repartition = df['Class'].value_counts().reset_index()
    df_repartition.columns = ['Type', 'Nombre']
    df_repartition['Type'] = df_repartition['Type'].replace({0: 'Légitime', 1: 'Fraude'})
    
    fig1 = px.bar(df_repartition, x='Type', y='Nombre', color='Type', 
                 log_y=True, # On utilise une échelle logarithmique car l'écart est géant
                 color_discrete_map={'Légitime': '#2ecc71', 'Fraude': '#e74c3c'})
    st.plotly_chart(fig1, use_container_width=True)

# --- ONGLET 2 : FACTEURS DE RISQUE ---
with onglet2:
    st.subheader("Quelles variables influencent le plus le modèle ?")
    st.write("Dans ce dataset, les variables sont anonymisées (V1, V2...). Voici celles qui permettent le mieux de détecter une fraude :")
    
    # Calcul de l'importance des variables (Feature Importance)
    importances = pd.Series(model.feature_importances_, index=model_columns)
    top_10_variables = importances.nlargest(10).reset_index()
    top_10_variables.columns = ['Variable', 'Importance']
    
    fig2 = px.bar(top_10_variables, x='Importance', y='Variable', orientation='h',
                 color='Importance', color_continuous_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("Les variables comme V17, V14 et V12 sont souvent les plus révélatrices d'un comportement suspect.")

# --- ONGLET 3 : TESTEUR DE TRANSACTION ---
with onglet3:
    st.subheader("Simuler une nouvelle transaction")
    st.write("Ajustez les paramètres pour voir comment le modèle réagit :")
    
    with st.form("form_fraude"):
        c1, c2 = st.columns(2)
        
        with c1:
            montant_input = st.number_input("Montant de la transaction ($)", 0.0, 20000.0, 100.0)
            v17_input = st.slider("Valeur de la variable V17 (Risque)", -20.0, 20.0, 0.0)
            
        with c2:
            v14_input = st.slider("Valeur de la variable V14 (Risque)", -20.0, 20.0, 0.0)
            v12_input = st.slider("Valeur de la variable V12 (Risque)", -20.0, 20.0, 0.0)
            
        bouton_test = st.form_submit_button("Lancer l'analyse")
        
        if bouton_test:
            # --- PRÉPARATION DES DONNÉES (Méthode explicite) ---
            donnees_test = {}
            for col in model_columns:
                donnees_test[col] = 0 # On initialise toutes les variables anonymes à 0
                
            # On injecte les valeurs du formulaire
            donnees_test['Amount'] = montant_input
            donnees_test['V17'] = v17_input
            donnees_test['V14'] = v14_input
            donnees_test['V12'] = v12_input
            
            # Conversion pour le modèle
            df_test = pd.DataFrame([donnees_test])
            
            # Prédiction
            probabilite_fraude = model.predict_proba(df_test)[0][1]
            
            st.markdown("---")
            st.write(f"Probabilité de fraude détectée : **{probabilite_fraude*100:.2f}%**")
            st.progress(probabilite_fraude)
            
            if probabilite_fraude > 0.5:
                st.error("### ALERTE : Transaction suspectée FRAUDULEUSE")
                st.write("Le modèle recommande de bloquer cette transaction pour vérification.")
            else:
                st.success("### VALIDÉ : Transaction probablement LÉGITIME")
                st.write("Le risque est considéré comme acceptable.")

# --- FOOTER ---
st.markdown("---")
st.caption("Développé par Fofana Abdou — Data Analyst Finance & Risk")
