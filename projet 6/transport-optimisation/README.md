# Optimisation des Coûts de Transport — Simulateur de Scénarios

## Problème business
Les dépenses de transport (fret) représentent un centre de coût massif pour l'entreprise. Bien souvent, la rapidité (transport aérien) est privilégiée par défaut, même quand l'urgence n'est pas absolue, ce qui fait exploser les marges. Le but de ce projet est d'auditer les pratiques d'expédition actuelles et de simuler les économies drastiques que l'on pourrait réaliser en basculant une partie du fret vers des modes de transport plus économiques (maritime, routier) tout en gardant un oeil sur le compromis du délai.

## Résultats clés (vrais chiffres)
- **Coût total des expéditions analysées** : 68 817 849 $
- **Principale anomalie identifiée** : Sur-utilisation coûteuse de l'aérien pour des colis lourds.

## Demo live (lien à compléter)
[Lien de l'application Streamlit à insérer ici après déploiement]

## Stack technique
Python · Pandas (Analyse) · Streamlit (Interface) · Plotly (Visualisation)

## Structure du projet
```
transport-optimisation/
├── app/
│   └── streamlit_app.py        # Interface web et simulateur de réduction de coûts
├── data/
│   └── SCMS_Delivery_History_Dataset.csv
├── notebooks/
│   ├── 01_exploration.ipynb    # Compréhension des coûts par mode et délai
│   ├── 02_analyse.ipynb        # Identification des surcoûts et calcul d'économie
│   ├── doc_exploration.md      # Doc pédagogique sur le nettoyage et la donnée
│   └── doc_analyse.md          # Doc pédagogique sur la chasse aux aberrations
├── README.md
└── requirements.txt
```

## Lancer en local
```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
streamlit run app/streamlit_app.py
```

## Ce que j'ai appris
1. **Nettoyage complexe de la donnée financière** : Les bases logistiques sont remplies d'exceptions textuelles (ex: "Invoiced Separately"). J'ai appris à assainir ces données pour pouvoir faire des mathématiques dessus.
2. **Identification des valeurs aberrantes (Outliers)** : J'ai mis en place un système de détection statistique (Moyenne + 2 Écarts-Types) pour traquer automatiquement les expéditions sur-facturées ou hors process.
3. **Création d'un Simulateur Métier** : La vraie valeur de l'analyse de données n'est pas dans le constat du passé, mais dans la projection. Construire un simulateur interactif permet aux managers de voir immédiatement les millions de dollars qu'ils peuvent économiser en modifiant la stratégie d'expédition (ex: passer 20% de l'Aérien en Maritime).
