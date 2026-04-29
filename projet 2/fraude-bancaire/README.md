# Détection de Fraude Bancaire

## Problème business
La fraude à la carte bancaire représente des millions d'euros de pertes chaque année pour les institutions financières. Le défi majeur est le déséquilibre extrême des données : dans ce dataset, seulement 0.17% des transactions sont frauduleuses (492 sur 284 807). J'ai conçu ce projet pour identifier ces comportements suspects sans impacter l'expérience des clients honnêtes.

## Résultats clés
- **Taux de fraude** : 0.17% (492 transactions frauduleuses détectées)
- **Recall (Rappel)** : 0.7449 (Je parviens à identifier 74.5% des fraudes réelles)
- **AUC-PR** : 0.8542 (Une performance très robuste sur des données déséquilibrées)
- **Top 3 facteurs** : Variables V17, V14 et V12 (issues de la décomposition PCA)

## Demo live
[Application interactive](https://fraude-bancaire-uh7zuiuytsizl7wcq6dkd9.streamlit.app/)

## Stack technique
Python · Pandas · Scikit-learn · SHAP · Streamlit · Plotly

## Structure du projet
```text
.
├── app/
│   ├── streamlit_app.py      # Application de monitoring
│   ├── model.joblib          # Modèle Random Forest
│   └── model_columns.joblib  # Liste des variables
├── data/
│   └── creditcard.csv        # Dataset source
├── notebooks/
│   ├── 01_exploration.ipynb  # Étude exploratoire
│   ├── 02_modele.ipynb       # Construction du modèle
│   ├── doc_exploration.md    # Guide pédagogique exploration
│   └── doc_modele.md         # Guide pédagogique modélisation
├── requirements.txt          # Dépendances
└── README.md
```

## Lancer en local
```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
streamlit run app/streamlit_app.py
```

## Ce que j'ai appris
1. **Métriques de vérité** : J'ai appris que l'AUC-ROC est souvent trop optimiste sur des données rares. L'AUC-PR est bien plus exigeante et m'a permis d'affiner mon modèle de manière plus honnête.
2. **Pondération des classes** : L'utilisation de `class_weight='balanced'` a été déterminante pour forcer le modèle à ne pas ignorer la fraude, malgré sa rareté extrême.
3. **Expliquabilité** : En finance, un modèle performant est inutile s'il n'est pas explicable. SHAP m'a permis de transformer une "boîte noire" en un outil d'aide à la décision pour les enquêteurs.
