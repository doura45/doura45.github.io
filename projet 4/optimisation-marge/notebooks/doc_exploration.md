# Guide du Débutant : Explorer des données avec DuckDB et Polars

Bienvenue dans mon guide pour l'analyse des ventes retail ! 
Si tu débutes en Data Science, tu as probablement l'habitude d'utiliser **Pandas**. Ici, j'ai choisi deux outils plus modernes et beaucoup plus rapides : **Polars** et **DuckDB**.

---

### 1. Pourquoi j'utilise Polars ?
Polars est comme une voiture de course comparée à Pandas. 
- Il charge les données CSV de manière incroyablement rapide.
- Il utilise tous les cœurs de ton processeur en même temps (multithreading).
- J'utilise Polars pour lire les fichiers Olist et effectuer les calculs mathématiques finaux.

### 2. Pourquoi j'utilise DuckDB ?
Faire des jointures (relier plusieurs tableaux entre eux) est souvent compliqué en Python pur.
- **DuckDB** me permet d'écrire du **SQL classique** (le langage des bases de données) directement dans mon notebook !
- Pas besoin de base de données externe : il interroge directement mes DataFrames Polars avec une vitesse fulgurante.
- J'ai utilisé DuckDB pour relier les commandes, les produits et les vendeurs dans une seule grande table de travail.

### 3. La réalité du dataset Olist
Un constat s'impose dans ce projet : Olist ne fournit pas les coûts des produits ou de fabrication. Sans coût, il est impossible de calculer une véritable marge brute. 
- **La solution** : J'utilise le Chiffre d'Affaires (CA) réel, basé sur le prix de vente payé par le client, comme indicateur de performance. C'est la métrique la plus solide pour mesurer l'attractivité des produits et la puissance commerciale des vendeurs.

### 4. Ce que j'ai découvert
En croisant les données, on observe que le chiffre d'affaires n'est pas réparti de manière équitable. Quelques catégories phares et un petit groupe de "Top Vendeurs" concentrent la majorité des revenus de la plateforme.
