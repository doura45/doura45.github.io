# Pilotage budgétaire retail — v2 : Analyse d'écarts et compte de résultat analytique

## 📋 Présentation & Problématique Business

La v1 d'un tableau de bord de gestion se contente généralement de dresser un constat (*« Écart moyen budget vs réalisé de 12,2% »*). **Ce projet v2 transforme ce constat en un outil d'aide à la décision stratégique pour la Direction Financière (CFO).**

Un écart brut n'a aucune valeur décisionnelle tant qu'il n'est pas **décomposé en causes actionnables**. Une direction générale ne peut pas agir sur un chiffre isolé ; elle peut en revanche arbitrer entre une baisse de volume sur une sous-gamme, une inflation du coût d'achat fournisseur ou une dégradation du mix produit.

---

## 💡 Hypothèses de Valorisation & Périmètre

> **Encadré de Valorisation**
> - **Périmètre :** 5 catégories de produits retail (*Électronique, Mode & Textile, Maison & Déco, Beauté & Santé, Sport & Loisirs*) suivies sur 12 mois.
> - **Source des données :** Jeu de données consolidé mensuel (`donnees_budget_realise_retail.csv`).
> - **Méthode de construction du budget :**
>   1. *Base :* Volume de référence par catégorie (`base_qte`), calibré comme un niveau d'activité annuel moyen.
>   2. *Saisonnalité :* Coefficient mensuel unique appliqué à toutes les catégories (pic T4, creux janvier/février), cf. `seasonality` dans `generate_cdg_data.py`.
>   3. *Prix budgété :* Fixe par catégorie sur l'année (`base_price`), le réel s'en écarte de −3 % à +2 % selon les mois.
>   4. *Limite assumée :* ce jeu de données est synthétique (pas de véritable historique N-1) — la méthode documente comment le budget est *simulé*, pas une reconstruction d'un historique réel.
> - **Taux & Ratios retenus :**
>   - *Taux de possession du stock :* **20% par an** (capital immobilisé, entreposage, obsolescence).
>   - *Taux de TVA :* 20% appliqué pour la conversion du CA et des achats TTC (calcul DSO/DPO).
> - **Seuil de Matérialité :** Commentaire automatique pour tout écart **$> 5\%$** ou **$> 10\text{ k€}$.**
> - **Limites :** Le modèle n'intègre pas les effets d'élasticité prix de second ordre.

---

## 🧮 Conventions & Formules Mathématiques Implémentées

### 1. Décomposition de l'Écart de Chiffre d'Affaires
Convention retenue : Écart = Réel − Budget.

$$\text{Écart Total CA} = (Q_r \times P_r) - (Q_b \times P_b)$$
$$\text{Écart sur Volume} = (Q_r - Q_b) \times P_b$$
$$\text{Écart sur Prix} = (P_r - P_b) \times Q_r \quad \text{(absorbant l'effet conjoint)}$$

### 2. Décomposition de l'Écart de Marge Brute
$$\text{Marge unitaire budget } m_{b,i} = P_{b,i} - C_{b,i}$$
$$\text{Écart sur Quantité} = (Q_r - Q_b) \times (P_b - C_b)$$
$$\text{Écart sur Prix de Vente} = (P_r - P_b) \times Q_r$$
$$\text{Écart sur Coût d'Achat} = -(C_r - C_b) \times Q_r$$

*(Le signe négatif sur le coût d'achat traduit le fait qu'une hausse de coût dégrade la marge).*

### 3. Isolation de l'Effet Mix (Multi-catégories)
$$\bar{m}_b = \frac{\sum (Q_{b,i} \times m_{b,i})}{\sum Q_{b,i}} \quad \text{(Marge unitaire moyenne pondérée budget)}$$
$$\text{Écart de Volume Pur} = (Q_{\text{total},r} - Q_{\text{total},b}) \times \bar{m}_b$$
$$\text{Écart de Mix} = \sum_i \left[ Q_{\text{total},r} \times (mix_{r,i} - mix_{b,i}) \times (m_{b,i} - \bar{m}_b) \right]$$

### 4. Compte de Résultat Analytique & Seuil de Rentabilité
$$\text{MCV (Marge sur Coûts Variables)} = \text{Marge Brute} - \text{Autres Coûts Variables}$$
$$\text{Taux de MCV} = \frac{\text{MCV}}{\text{CA}}$$
$$\text{Seuil de Rentabilité (SR en CA)} = \frac{\text{Coûts Fixes Affectés}}{\text{Taux de MCV}}$$
$$\text{Point Mort (en jours)} = \left(\frac{\text{SR}}{\text{CA Annuel}}\right) \times 365$$
$$\text{Levier Opérationnel} = \frac{\text{MCV}}{\text{Résultat Analytique}}$$

### 5. Stocks, BFR et Cash
$$\text{Rotation des Stocks} = \frac{\text{COGS Annuel}}{\text{Stock Moyen}}$$
$$\text{Coût de Possession} = \text{Stock Moyen} \times 20\%$$
$$\text{DSO (Délai Clients)} = \left(\frac{\text{Créances Clients}}{\text{CA TTC}}\right) \times 365$$
$$\text{DPO (Délai Fournisseurs)} = \left(\frac{\text{Dettes Fournisseurs}}{\text{Achats TTC}}\right) \times 365$$

### 6. Atterrissage (Rolling Forecast à 2 Scénarios)
* **Scénario A (Tendanciel) :** Réalisé cumulé à date + (Budget mois restants $\times$ Taux de réalisation à date).
* **Scénario B (Retour Norme) :** Réalisé cumulé à date + Budget initial des mois restants.

---

## 📂 Structure du Dépôt

```text
cdg-public/
├── data/
│   └── donnees_budget_realise_retail.csv   # Base de données 12 mois x 5 catégories
├── excel/
│   └── Pilotage_Budgetaire_Retail_v2.xlsx  # Classeur Excel complet à 5 onglets
├── scripts/
│   ├── generate_cdg_data.py                # Script de génération du dataset
│   └── calculs_cdg_engine.py               # Moteur de calcul des écarts & export Excel
├── commentaire_de_gestion_mensuel.md       # Note de synthèse 1 page pour la Direction (CFO-ready)
└── README.md                               # Documentation technique et méthodologique
```

---

## 🛠️ Utilisation en Local

```bash
# 1. Générer la base de données
python3 scripts/generate_cdg_data.py

# 2. Exécuter le moteur de calculs et générer le classeur Excel
python3 scripts/calculs_cdg_engine.py
```

---
*Projet réalisé par Fofana Abdou — Expert Contrôle de Gestion & Financial Data Analytics*
