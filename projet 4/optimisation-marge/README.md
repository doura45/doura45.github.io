# Optimisation du Chiffre d'Affaires — Analyse Retail

Analyse approfondie de la performance commerciale e-commerce (données Olist) en utilisant des technologies modernes et ultra-rapides.

## Problème business
Identifier les véritables moteurs de croissance au sein du catalogue produit et des vendeurs partenaires. L'objectif est d'utiliser le Chiffre d'Affaires comme proxy de la performance pour purger le catalogue des produits et vendeurs sous-performants qui parasitent la plateforme.

## Résultats clés (vrais chiffres)
- **Chiffre d'Affaires Total** : $13 221 498
- **Chiffre d'Affaires Moyen par Commande** : $137.04

## Demo live
[Application interactive Streamlit](https://optimisation-marge-pxthm6hicdjs8cfx2ejevs.streamlit.app/)

## Stack technique
Python · DuckDB (SQL Engine) · Polars (DataFrame) · Streamlit · Plotly

## Structure du projet
```text
optimisation-marge/
├── app/
│   └── streamlit_app.py      # Interface utilisateur et Simulateur de CA
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_products_dataset.csv
│   └── olist_sellers_dataset.csv
├── notebooks/
│   ├── 01_exploration.ipynb  # Analyse exploratoire (DuckDB/Polars)
│   ├── 02_analyse.ipynb      # Analyse Vendeurs et Temporalité
│   ├── doc_exploration.md    # Guide pédagogique (Polars/DuckDB)
│   └── doc_analyse.md        # Guide pédagogique (Vendeurs/Temps)
├── requirements.txt          # Dépendances (polars, duckdb, etc.)
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
1. **Performance Polars vs Pandas** : J'ai découvert la puissance de Polars pour charger et manipuler des données volumineuses sans saturer la RAM.
2. **Puissance de DuckDB** : Faire des jointures SQL complexes directement sur des DataFrames locaux est un gain de temps énorme.
3. **Simulateur Temps Réel** : J'ai appris à construire un simulateur de revenus interactif permettant de mesurer l'impact de différents scénarios de croissance (prix/volume) en direct.
