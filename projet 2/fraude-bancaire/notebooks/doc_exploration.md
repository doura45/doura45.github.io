# 📚 Guide : Comprendre l'Exploration des Données de Fraude

Dans cette première étape, j'ai analysé les transactions pour comprendre comment les fraudeurs opèrent. Voici les concepts clés que j'ai utilisés :

### 1. Le Déséquilibre des Classes (Imbalance)
C'est le point le plus important. Dans ce dataset, il y a environ 284 000 transactions normales pour seulement 492 fraudes. 
- **Ce que ça signifie** : Si je crée un modèle qui dit "Tout est normal", il aura 99.8% de précision mais ratera toutes les fraudes. 
- **Ma solution** : Je dois utiliser des graphiques en échelle logarithmique pour pouvoir visualiser la fraude.

### 2. L'Analyse des Montants (Amount)
J'ai comparé la somme d'argent dépensée dans les transactions normales vs frauduleuses.
- **Constat** : Les fraudes ne sont pas forcément de très gros montants. Elles sont souvent diluées parmi les petites transactions pour ne pas alerter les banques.

### 3. Pourquoi l'Accuracy ne sert à rien ici ?
L'Accuracy mesure le nombre de bonnes réponses globales. Ici, elle est inutile car le but n'est pas d'être bon sur les 99.8% de clients honnêtes, mais d'attraper les 0.2% de voleurs.
