# Mon Approche : Modélisation et Prédiction du Churn

Ce document détaille la méthodologie que j'ai suivie pour construire un modèle capable de prédire le départ des clients.

---

## 1. Méthodologie

### ✂️ Découpage des données (Train/Test Split)
Avant d'entraîner mon modèle, j'ai divisé mes données en deux ensembles :
- **Entraînement (80%)** : Les données que le modèle étudie pour apprendre les motifs de départ.
- **Test (20%)** : Les données "inconnues" sur lesquelles je teste le modèle pour vérifier sa capacité de généralisation.

### 🌳 Le choix du Random Forest
J'ai choisi cet algorithme car il est particulièrement robuste. Il combine plusieurs "arbres de décision" pour stabiliser les prédictions. Chaque arbre vote, et la décision finale est prise à la majorité, ce qui permet de capturer des relations complexes entre les variables sans tomber dans le sur-apprentissage.

---

## 2. Évaluation de la Performance

### 🎯 L'importance du Recall
Pour ce projet, j'ai décidé de privilégier le **Recall (Rappel)** plutôt que l'Accuracy. Dans un contexte business de churn, je considère qu'il est bien plus grave de rater un client qui va partir (perte de revenu) que de se tromper sur un client fidèle (coût minime d'une offre promotionnelle). 

- **AUC-ROC** : Ce score de 0.82 me confirme que mon modèle distingue très bien les deux classes de clients.
- **Recall** : J'ai réussi à atteindre un score de 0.71, ce qui signifie que je détecte plus de 70% des futurs départs.

---

## 3. Interprétation avec SHAP

### 💡 Pourquoi j'utilise SHAP ?
Je refuse l'effet "boîte noire". J'utilise SHAP pour apporter de la transparence aux prédictions :
- **Transparence** : SHAP m'explique précisément l'impact de chaque variable (type de contrat, prix, ancienneté) sur le score de risque.
- **Action métier** : Cela me permet de conseiller des actions concrètes. Si je vois que c'est le prix qui fait fuir un client, je peux suggérer une remise ciblée.

## ⚡ Stratégies d'optimisation

### 1. Ajustement du Seuil de Décision
J'ai abaissé le seuil de prédiction de 0.5 à 0.3. En étant plus "sensible", mon modèle lève l'alerte plus tôt. C'est un choix délibéré : je préfère une légère baisse de précision au profit d'une détection maximale des risques.

### 2. Équilibrage des classes (Class Weighting)
Puisque les clients qui restent sont majoritaires, j'ai appliqué un poids plus fort à la classe "Churn" durant l'entraînement. J'ai ainsi forcé l'algorithme à accorder plus d'importance aux exemples de départ, ce qui a mécaniquement boosté ma capacité de détection.
