# Analyse du Churn Client — Secteur Bancaire

## Problème business
Dans le secteur bancaire, 26.5% des clients quittent leur établissement chaque année. Ce projet identifie les profils à risque et les causes principales du départ pour permettre une action préventive ciblée. J'ai cherché à comprendre pourquoi certains clients sont plus enclins à partir et comment nous pourrions les retenir plus efficacement.

## Résultats clés
- Taux de churn global : 26.5%
- Modèle Random Forest : détecte 71% des clients à risque (Recall 0.714)
- AUC-ROC : 0.820
- Top 3 causes : ancienneté faible, contrat mensuel, mensualités élevées

## Demo live
[Application interactive](https://churn-finance-analyse-rbp3gik2mgpd3agnkjure2.streamlit.app/)

## Stack technique
Python · Pandas · Scikit-learn · SHAP · Streamlit · Plotly

## Structure du projet
```text
.
├── app/
│   ├── streamlit_app.py      # Application interactive
│   ├── model.joblib          # Modèle entraîné
│   └── model_columns.joblib  # Colonnes de features
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── notebooks/
│   ├── 01_exploration.ipynb  # Analyse exploratoire
│   ├── 02_modele.ipynb       # Entraînement et évaluation
│   ├── doc_exploration.md    # Documentation d'analyse
│   └── doc_modele.md         # Documentation technique
├── requirements.txt          # Dépendances
└── README.md
```

## Lancer en local
```bash
# 1. Cloner le projet
git clone https://github.com/doura45/churn-finance-analyse.git

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app/streamlit_app.py
```

## Ce que j'ai appris
1. **Équilibre Précision-Recall** : J'ai appris que dans un contexte métier de churn, il est préférable de sur-détecter les départs (Recall élevé) quitte à avoir quelques faux positifs, car le coût d'une campagne de rétention est souvent bien inférieur à la perte d'un client.
2. **Impact de l'Ancienneté** : L'analyse a révélé que les premiers mois sont critiques. J'ai constaté que le risque de churn chute drastiquement après la première année, ce qui suggère de concentrer les efforts sur l'onboarding.
3. **Interprétabilité des modèles** : L'utilisation de SHAP m'a permis d'ouvrir la "boîte noire" du Random Forest. J'ai pu expliquer concrètement pourquoi un client recevait un score de risque élevé, ce qui est indispensable pour convaincre les équipes métier de passer à l'action.
