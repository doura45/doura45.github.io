# Guide du Débutant : Explorer les Données de Transport

Pour optimiser des coûts logistiques, il faut d'abord comprendre comment et où on dépense l'argent. C'est l'objectif de cette exploration.

---

### 1. Le Nettoyage (Le sale boulot)
Dans ce fichier (comme souvent dans la Supply Chain), beaucoup de prix et de poids n'étaient pas des nombres, mais du texte (ex: "See ERP" signifiant que le prix est dans un autre logiciel). 
J'ai dû utiliser Pandas pour :
- Remplacer ces textes par des valeurs vides (NaN).
- Convertir le reste en vrais chiffres.
- Soustraire la `Date d'expédition` à la `Date de livraison` pour obtenir un "Délai" en jours.

### 2. Les Modes de Transport
J'ai groupé les données par `Shipment Mode` (Air, Ocean, Truck, Rail).
- **L'Aérien (Air)** : C'est le roi incontesté de nos données. Il coûte une fortune, mais c'est le plus rapide.
- **Le Maritime (Ocean)** : C'est l'inverse. C'est le moins cher, parfait pour les très gros volumes, mais c'est lent.

### 3. La relation Poids / Coût
Grâce à un graphique de dispersion (scatter plot), j'ai pu prouver visuellement que plus un colis est lourd, plus l'envoyer par les airs devient un gouffre financier. À l'inverse, par bateau, le poids impacte très peu le prix. 

**La conclusion est claire :** Le moyen le plus rapide et le plus violent de faire des économies est de transférer nos colis les plus lourds de l'avion vers le bateau. C'est ce que nous allons simuler dans la prochaine étape !
