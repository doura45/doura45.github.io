# Guide du Débutant : Analyse Vendeurs et Temporalité

Dans la suite de mon projet sur les ventes retail, je me suis concentré sur deux aspects essentiels d'une marketplace : les **vendeurs** et le **temps**.

---

### 1. Pourquoi analyser les vendeurs ?
Dans un modèle e-commerce classique comme Olist, la plateforme héberge de nombreux petits vendeurs.
- **La découverte** : La majorité des vendeurs réalisent un Chiffre d'Affaires (CA) très inférieur à la moyenne globale. Seule une poignée de "Top Vendeurs" porte le succès financier de la marketplace.
- **L'action business** : En tant que Data Analyst, mon rôle n'est pas juste de faire des graphiques, c'est de proposer des actions. Ici, ma recommandation est claire : il faut déployer un programme d'accompagnement ciblé pour aider la masse des petits vendeurs à générer plus de ventes.

### 2. Le facteur Temps (Évolution Mensuelle)
Vendre beaucoup à une période donnée (comme le Black Friday) est crucial pour le bilan annuel.
- J'ai utilisé Polars pour regrouper les données par mois de manière très rapide.
- Le suivi de la courbe du Chiffre d'Affaires m'aide à comprendre la saisonnalité du business.

### 3. La carte Volume vs CA
J'ai créé un graphique de dispersion (scatter plot).
- **En abscisse (X)** : Le volume de ventes.
- **En ordonnée (Y)** : Le Chiffre d'Affaires total.
- La taille des bulles représente le prix moyen.
- **Pourquoi c'est puissant ?** : D'un seul coup d'œil, je peux voir quelles catégories dominent. L'idéal est d'avoir des grosses bulles en haut à droite. Les catégories en bas à droite (beaucoup de ventes, mais faible CA) révèlent des produits peu chers qui saturent peut-être la chaîne logistique sans rapporter beaucoup de revenus à la plateforme.
