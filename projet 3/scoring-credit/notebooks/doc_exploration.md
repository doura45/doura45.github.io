# Guide : Comprendre l'Exploration des Données de Crédit

Bienvenue dans ce guide ! J'ai conçu ce document pour t'aider à comprendre les étapes que j'ai suivies pour analyser les données de crédit bancaire.

---

### 1. Pourquoi explorer les données ?
Avant de construire un modèle de calcul (une intelligence mathématique), je dois comprendre ce qu'il y a dans mes fichiers. C'est comme faire l'inventaire d'un magasin avant de décider quoi vendre.

### 2. Le défi du "Déséquilibre"
Dans ce projet, j'ai constaté que seulement **8%** des clients ont des difficultés de paiement. 
- **Le problème** : Si je ne fais rien, mon futur modèle pourrait se contenter de dire "Tout le monde va payer" et il aurait raison 92% du temps. Mais il raterait tous les clients risqués !
- **Ma solution** : Je dois identifier ce déséquilibre dès maintenant pour pouvoir le corriger plus tard.

### 3. Les "Signaux d'Alarme" (Corrélations)
La corrélation est un chiffre entre -1 et 1 qui indique si deux choses sont liées.
- **EXT_SOURCE** : J'ai découvert que ces variables sont les plus importantes. Elles représentent des scores provenant d'organismes extérieurs. Plus elles sont élevées, plus le client est fiable.
- **L'Âge** : J'ai vu que les jeunes clients (ceux dont le nombre de jours depuis la naissance est plus faible) présentent statistiquement plus de risques.

### 4. La puissance de l'historique
J'ai relié mon fichier principal au fichier "Bureau". Pourquoi ?
- Parce que le comportement passé est souvent le meilleur prédicteur du comportement futur. 
- En comptant le nombre de crédits déjà contractés par un client ailleurs, j'ajoute une information précieuse à mon analyse.

### 5. Ce qu'il faut retenir
L'exploration m'a permis de voir que le risque n'est pas réparti au hasard. Il dépend fortement de l'historique externe et de l'âge du demandeur. C'est sur ces piliers que je vais construire mon modèle de prédiction.
