# 📚 Documentation : Concepts d'Analyse de Données

Ce document explique les outils et concepts utilisés dans notre notebook d'exploration. Il est conçu pour être accessible même si vous débutez en Python.

---

## 1. Bibliothèques Utilisées

### 🐼 Pandas
Pandas est la bibliothèque de référence pour manipuler des données en Python. 
- **Concept** : Elle utilise des "DataFrames", qui ressemblent à des tableaux Excel. 
- **Usage** : On l'utilise pour charger le fichier CSV, filtrer les données, calculer des moyennes ou compter le nombre de clients.

### 📊 Seaborn & Matplotlib
Ce sont nos outils de visualisation.
- **Matplotlib** : C'est la base. Elle permet de créer des graphiques simples (titres, axes, couleurs).
- **Seaborn** : C'est une surcouche de Matplotlib qui rend les graphiques plus beaux et plus faciles à coder pour des analyses statistiques.

---

## 2. Types de Graphiques Expliqués

### 🥧 Camembert (Pie Chart)
- **C'est quoi ?** Un cercle divisé en parts.
- **Pourquoi l'utiliser ?** Idéal pour montrer une répartition simple, comme le pourcentage de clients qui partent (Churn) par rapport à ceux qui restent.

### 📊 Diagramme en barres (Countplot)
- **C'est quoi ?** Des barres dont la hauteur représente une quantité.
- **Pourquoi l'utiliser ?** Parfait pour comparer des catégories, par exemple voir quel type de contrat (Mensuel, Annuel) a le plus de départs.

### 📦 Boîte à moustaches (Boxplot)
- **C'est quoi ?** Un rectangle avec des lignes qui dépassent. 
- **Pourquoi l'utiliser ?** Il montre la distribution des prix. Le rectangle représente les 50% des clients "du milieu". Cela permet de voir si les clients qui partent paient globalement plus cher que les autres.

---

## 3. Analyse de Corrélation
La corrélation mesure à quel point deux variables évoluent ensemble. 
- Si une variable augmente quand l'autre augmente, elles sont liées.
- Cela nous aide à identifier les "signaux d'alarme" (ex: un certain mode de paiement) avant qu'un client ne parte.
