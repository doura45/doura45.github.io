# Guide : Comment mon Modèle Prédit le Risque ?

Après avoir analysé les données, j'ai construit une "machine à prédire". Voici comment elle fonctionne, étape par étape.

---

### 1. La préparation des ingrédients (Fusion et Nettoyage)
Un modèle ne peut pas lire des fichiers séparés. 
- **La fusion** : J'ai regroupé les données de la demande actuelle avec l'historique du client. 
- **Le nettoyage** : Si des informations manquaient, je les ai remplacées par la valeur "médiane" (la valeur du milieu) pour ne pas perturber les calculs.
- **Le codage** : J'ai transformé les mots (comme "Marié" ou "Célibataire") en nombres, car les modèles ne comprennent que les chiffres.

### 2. L'algorithme : Le Random Forest (Forêt Aléatoire)
Imagine que tu demandes à 100 experts différents de donner leur avis sur un dossier de crédit. Chacun regarde les données un peu différemment. À la fin, ils votent.
- C'est exactement ce que fait le **Random Forest**. Il crée 100 "arbres de décision" et prend la moyenne de leurs votes pour être le plus juste possible.

### 3. Apprendre à voir les cas rares
Comme il y a très peu de clients en défaut (8%), j'ai dû dire au modèle : "Attention, rater un mauvais payeur est 10 fois plus grave que de se tromper sur un bon payeur". C'est ce qu'on appelle l'équilibrage des classes.

### 4. Comment savoir si ça marche ? (Les métriques)
J'utilise trois indicateurs clés :
- **AUC-ROC** : Mesure la capacité du modèle à classer un client risqué plus haut qu'un client sûr.
- **Recall (Rappel)** : Indique si j'ai réussi à attraper le plus grand nombre possible de clients risqués.
- **AUC-PR** : Estime la précision du modèle spécifiquement sur les cas de défaut.

### 5. L'explication : SHAP
Un modèle performant ne sert à rien si on ne comprend pas sa décision. 
- Grâce à l'outil **SHAP**, je peux te montrer exactement quelle variable (ton âge, ton revenu, ton score externe) a fait pencher la balance vers une acceptation ou un refus de crédit.
