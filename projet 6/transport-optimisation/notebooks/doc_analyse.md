# Guide du Débutant : Optimiser et Simuler

Après avoir compris où allait l'argent (voir l'exploration), l'objectif de cette deuxième partie est de trouver des moyens de réduire la facture.

---

### 1. Le Coût au Kilo (La métrique étalon)
C'est impossible de comparer un colis de 10 grammes avec un conteneur de 3 tonnes. Pour comparer l'efficacité des modes de transport, j'ai tout ramené au **Coût par Kilo**. Sans surprise, l'avion est de loin le plus cher par kilo.

### 2. La Traque des Anomalies (Les Écarts-Types)
Imaginons que tu prennes toujours le même trajet en Uber pour 10$. Un jour, ça te coûte 50$. C'est une anomalie.
En statistique, on utilise l'Écart-Type. J'ai configuré l'algorithme pour qu'il sonne l'alarme si une expédition coûte la moyenne habituelle + 2 fois l'écart-type. Résultat : J'ai trouvé des centaines de milliers de dollars gaspillés dans des expéditions "urgentes" ou mal négociées.

### 3. Le Simulateur de Basculement
C'est ici qu'on crée de la vraie valeur !
J'ai codé un simulateur : *"Que se passe-t-il si je force l'ordinateur à prendre 20% des colis envoyés par avion, et que je les met dans un bateau à la place ?"*
L'algorithme recalcule le prix de ces colis avec le tarif maritime. La différence entre le prix payé (avion) et le prix simulé (bateau) nous donne notre **Économie Nette**. Bien sûr, le délai de livraison augmente, c'est le compromis à accepter.
