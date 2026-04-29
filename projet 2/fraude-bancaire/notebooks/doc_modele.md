# 🧠 Guide : La Modélisation de la Fraude

Dans cette étape, je suis passé de l'analyse à la prédiction. Voici les décisions clés que j'ai prises pour construire mon modèle :

### 1. Le choix du Random Forest (Forêt Aléatoire)
J'ai choisi cet algorithme car il est très puissant pour traiter des relations non-linéaires. Dans le cas de la fraude, les comportements des voleurs changent tout le temps. Une forêt d'arbres est plus stable qu'un seul arbre.
- **Le réglage magique** : `class_weight='balanced'`. Puisque j'ai très peu de fraudes, je dis mathématiquement au modèle : "Une fraude ratée est bien plus grave qu'une transaction normale mal classée".

### 2. Pourquoi l'AUC-PR au lieu de l'AUC-ROC ?
C'est un point technique crucial :
- **AUC-ROC** : Elle regarde la performance globale. Sur un dataset où 99.8% des données sont "normales", elle aura toujours l'air excellente, même si le modèle est médiocre sur la fraude.
- **AUC-PR** : Elle se concentre uniquement sur la capacité du modèle à trouver la fraude (Recall) et à être sûr de lui quand il en trouve une (Précision). C'est la métrique de vérité pour les données déséquilibrées.

### 3. L'importance de SHAP
Un modèle performant ne suffit pas, il doit être explicable. 
- **Ce que je fais** : J'utilise SHAP pour voir quelles variables (V1, V2, etc.) ont poussé le modèle à dire "C'est une fraude". 
- **Bénéfice** : Cela permet aux enquêteurs de la banque de comprendre la "signature" d'une fraude et de justifier le blocage d'une carte.
