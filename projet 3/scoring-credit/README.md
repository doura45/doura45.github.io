# Scoring de Crédit — Évaluation du Risque Bancaire

Ce projet implémente un système de scoring crédit pour prédire la probabilité de défaut de paiement des demandeurs de prêt. Il utilise les données de demande actuelles enrichies par l'historique du Bureau de Crédit.

## Problème business
Le défi pour une institution financière est d'identifier avec précision les clients qui pourraient rencontrer des difficultés de remboursement. Un refus injustifié fait perdre un client fidèle, tandis qu'une acceptation risquée entraîne des pertes financières. Ce modèle aide à automatiser cette décision avec transparence.

## Résultats clés
- **AUC-ROC** : 0.703 (Performance stable sur l'échantillon de 16%)
- **Recall (Rappel)** : 0.477 (Détection équilibrée du risque de défaut)
- **AUC-PR** : 0.187 (Précision-Rappel robuste sur données originales)

## Demo live
[Application interactive](https://scoring-credit-hryuwvqx8qfj3mak2uwdee.streamlit.app/)

## Stack technique
Python · Pandas · Scikit-learn · Random Forest · SHAP · Streamlit · Plotly

## Structure du projet
```text
.
├── app/
│   ├── streamlit_app.py      # Interface utilisateur
│   ├── model.joblib          # Modèle entraîné
│   └── model_columns.joblib  # Variables utilisées
├── data/
│   ├── application_train.csv # Données clients (échantillonnées pour GitHub)
│   └── bureau.csv            # Historique bureau
├── notebooks/
│   ├── 01_exploration.ipynb  # Analyse exploratoire
│   ├── 02_modele.ipynb       # Entraînement et évaluation
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
1. **Gestion du déséquilibre** : J'ai appris à utiliser des poids de classe équilibrés pour forcer le modèle à ne pas ignorer la minorité de clients en défaut.
2. **Interprétabilité SHAP** : J'ai compris l'importance d'expliquer pourquoi un crédit est refusé. Les variables externes sont les plus influentes.
3. **Optimisation des jointures** : L'agrégation des données du bureau a été cruciale pour capturer l'historique complet du client dans une seule ligne.
