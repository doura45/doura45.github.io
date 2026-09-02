#!/usr/bin/env python3
"""
Générateur de données de pilotage budgétaire retail v2 (Stdlib Python - Aucun paquet externe).
Produit un jeu de données de 60 lignes (12 mois x 5 catégories) avec l'ensemble des métriques CDG.
"""

import os
import csv
import random

def generate_retail_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    categories = [
        {"name": "Electronique", "base_qte": 1200, "base_price": 250.0, "base_cost": 175.0, "var_cost_pct": 0.05, "fixed_monthly": 15000},
        {"name": "Mode & Textile", "base_qte": 4500, "base_price": 45.0, "base_cost": 18.0, "var_cost_pct": 0.08, "fixed_monthly": 20000},
        {"name": "Maison & Deco", "base_qte": 2200, "base_price": 85.0, "base_cost": 45.0, "var_cost_pct": 0.06, "fixed_monthly": 14000},
        {"name": "Beaute & Sante", "base_qte": 5800, "base_price": 30.0, "base_cost": 9.0, "var_cost_pct": 0.04, "fixed_monthly": 12000},
        {"name": "Sport & Loisirs", "base_qte": 1800, "base_price": 110.0, "base_cost": 60.0, "var_cost_pct": 0.07, "fixed_monthly": 10000},
    ]

    months = [f"2025-{m:02d}" for m in range(1, 13)]
    seasonality = [0.85, 0.80, 0.90, 0.95, 1.05, 1.10, 1.15, 0.90, 1.00, 1.05, 1.25, 1.40]
    
    random.seed(42)

    fieldnames = [
        "periode", "categorie", "qte_budget", "qte_reelle",
        "pu_vente_budget", "pu_vente_reel", "cout_achat_unit_budget", "cout_achat_unit_reel",
        "couts_variables_autres", "couts_fixes_affectes",
        "stock_debut", "stock_fin", "creances_clients", "dettes_fournisseurs"
    ]

    rows = []

    for idx, month in enumerate(months):
        seas_factor = seasonality[idx]
        
        for cat in categories:
            qte_budget = int(cat["base_qte"] * seas_factor)
            
            if cat["name"] == "Mode & Textile" and idx in [5, 6, 7]:
                vol_variance = random.uniform(-0.14, -0.08)
            elif cat["name"] == "Electronique" and idx in [8, 9, 10]:
                vol_variance = random.uniform(-0.10, -0.04)
            else:
                vol_variance = random.uniform(-0.06, 0.04)
                
            qte_reelle = int(round(qte_budget * (1 + vol_variance)))

            pu_vente_budget = cat["base_price"]
            price_variance = random.uniform(-0.03, 0.02)
            pu_vente_reel = round(pu_vente_budget * (1 + price_variance), 2)

            cout_achat_unit_budget = cat["base_cost"]
            cost_variance = random.uniform(0.01, 0.045) if idx >= 4 else random.uniform(-0.01, 0.02)
            cout_achat_unit_reel = round(cout_achat_unit_budget * (1 + cost_variance), 2)

            ca_reel = qte_reelle * pu_vente_reel
            couts_variables_autres = round(ca_reel * cat["var_cost_pct"] * random.uniform(0.95, 1.08), 2)

            couts_fixes_affectes = round(cat["fixed_monthly"] * random.uniform(0.98, 1.02), 2)

            cogs_mensuel = qte_reelle * cout_achat_unit_reel
            stock_debut = round(cogs_mensuel * random.uniform(1.2, 1.6), 2)
            stock_fin = round(stock_debut + cogs_mensuel * random.uniform(-0.1, 0.15), 2)

            dso_jours = 25 + idx * 0.35 + random.uniform(-2, 2)
            creances_clients = round((ca_reel * 1.20) * (dso_jours / 30), 2)

            dpo_jours = 45 + random.uniform(-4, 4)
            achats_mensuels_ttc = (cogs_mensuel * 1.20)
            dettes_fournisseurs = round(achats_mensuels_ttc * (dpo_jours / 30), 2)

            rows.append({
                "periode": month,
                "categorie": cat["name"],
                "qte_budget": qte_budget,
                "qte_reelle": qte_reelle,
                "pu_vente_budget": pu_vente_budget,
                "pu_vente_reel": pu_vente_reel,
                "cout_achat_unit_budget": cout_achat_unit_budget,
                "cout_achat_unit_reel": cout_achat_unit_reel,
                "couts_variables_autres": couts_variables_autres,
                "couts_fixes_affectes": couts_fixes_affectes,
                "stock_debut": stock_debut,
                "stock_fin": stock_fin,
                "creances_clients": creances_clients,
                "dettes_fournisseurs": dettes_fournisseurs
            })

    csv_path = os.path.join(data_dir, "donnees_budget_realise_retail.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Données générées avec succès : {csv_path} ({len(rows)} lignes)")
    return csv_path

if __name__ == "__main__":
    generate_retail_data()
