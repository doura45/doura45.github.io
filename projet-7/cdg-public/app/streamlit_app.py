import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Pilotage Budgétaire Retail v2 — Contrôle de Gestion",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement des données
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "donnees_budget_realise_retail.csv")

    # data/ est exclu du dépôt (.gitignore) : régénéré à la volée si absent (ex. déploiement Streamlit Cloud)
    if not os.path.exists(csv_path):
        sys.path.insert(0, os.path.join(base_dir, "scripts"))
        from generate_cdg_data import generate_retail_data
        generate_retail_data()

    df = pd.read_csv(csv_path)
    
    # Métriques dérivées
    df["ca_budget"] = df["qte_budget"] * df["pu_vente_budget"]
    df["ca_reel"] = df["qte_reelle"] * df["pu_vente_reel"]
    df["cogs_budget"] = df["qte_budget"] * df["cout_achat_unit_budget"]
    df["cogs_reel"] = df["qte_reelle"] * df["cout_achat_unit_reel"]
    df["marge_brute_budget"] = df["ca_budget"] - df["cogs_budget"]
    df["marge_brute_reel"] = df["ca_reel"] - df["cogs_reel"]
    df["mcv"] = df["marge_brute_reel"] - df["couts_variables_autres"]
    df["resultat_analytique"] = df["mcv"] - df["couts_fixes_affectes"]
    return df

df = load_data()

# Barre latérale - Filtres
st.sidebar.title("🎛️ Pilotage & Filtres")
st.sidebar.markdown("---")

selected_months = st.sidebar.multiselect(
    "Filtrer par Période (Mois)",
    options=sorted(df["periode"].unique()),
    default=sorted(df["periode"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Filtrer par Catégorie",
    options=sorted(df["categorie"].unique()),
    default=sorted(df["categorie"].unique())
)

# Filtrage du DataFrame
df_filtered = df[(df["periode"].isin(selected_months)) & (df["categorie"].isin(selected_categories))]

# Titre Principal
st.title("📊 Pilotage Budgétaire Retail v2 — Contrôle de Gestion")
st.markdown("**Analyse d'Écarts, Compte de Résultat Analytique, Seuil de Rentabilité & Rolling Forecast**")
st.markdown("---")

# Navigation par Onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Synthèse & Bridge Waterfall",
    "🔍 Décomposition des Écarts & Mix",
    "📑 Compte de Résultat Analytique",
    "💼 Stock, BFR & Rolling Forecast",
    "📝 Commentaire de Gestion (CFO Note)"
])

# -----------------------------------------------------------------------------
# TAB 1 : SYNTHÈSE & BRIDGE WATERFALL
# -----------------------------------------------------------------------------
with tab1:
    ca_b = df_filtered["ca_budget"].sum()
    ca_r = df_filtered["ca_reel"].sum()
    ecart_ca = ca_r - ca_b
    ecart_ca_pct = (ecart_ca / ca_b) * 100 if ca_b > 0 else 0

    mb_b = df_filtered["marge_brute_budget"].sum()
    mb_r = df_filtered["marge_brute_reel"].sum()
    ecart_mb = mb_r - mb_b

    mcv_r = df_filtered["mcv"].sum()
    res_r = df_filtered["resultat_analytique"].sum()

    # KPI Top Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("CA Réel", f"{ca_r:,.0f} €", f"{ecart_ca_pct:+.1f}% vs Budget")
    col2.metric("Marge Brute Réelle", f"{mb_r:,.0f} €", f"{(mb_r - mb_b):+,.0f} €")
    col3.metric("MCV Réelle", f"{mcv_r:,.0f} €", f"Taux MCV: {(mcv_r/ca_r*100):.1f}%")
    col4.metric("Résultat Analytique", f"{res_r:,.0f} €", f"{(res_r/ca_r*100):.1f}% du CA")
    col5.metric("Écart Total CA", f"{ecart_ca:,.0f} €", delta_color="normal")

    st.markdown("### 🌉 Bridge Waterfall : Passage du CA Budget au CA Réel")
    
    # Calculs pour le Waterfall CA
    qte_b = df_filtered["qte_budget"].sum()
    qte_r = df_filtered["qte_reelle"].sum()
    pu_b_avg = ca_b / qte_b if qte_b > 0 else 0
    pu_r_avg = ca_r / qte_r if qte_r > 0 else 0
    
    ecart_vol = (qte_r - qte_b) * pu_b_avg
    ecart_prix = (pu_r_avg - pu_b_avg) * qte_r

    fig_waterfall = go.Figure(go.Waterfall(
        name = "Waterfall CA",
        orientation = "v",
        measure = ["absolute", "relative", "relative", "total"],
        x = ["CA Budget", "Écart Volume", "Écart Prix", "CA Réel"],
        textposition = "outside",
        text = [f"{ca_b:,.0f} €", f"{ecart_vol:,.0f} €", f"{ecart_prix:,.0f} €", f"{ca_r:,.0f} €"],
        y = [ca_b, ecart_vol, ecart_prix, ca_r],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#EF4444"}},
        increasing = {"marker":{"color":"#10B981"}},
        totals = {"marker":{"color":"#1F4E79"}}
    ))

    fig_waterfall.update_layout(
        title="Pont de variation du Chiffre d'Affaires (€)",
        showlegend = False,
        height=450
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2 : DÉCOMPOSITION DES ÉCARTS & MIX
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("🔍 Décomposition Analytique des Écarts par Catégorie")
    
    cat_agg = df_filtered.groupby("categorie").agg({
        "qte_budget": "sum", "qte_reelle": "sum",
        "ca_budget": "sum", "ca_reel": "sum",
        "cogs_budget": "sum", "cogs_reel": "sum",
        "marge_brute_budget": "sum", "marge_brute_reel": "sum"
    }).reset_index()

    cat_agg["pu_b"] = cat_agg["ca_budget"] / cat_agg["qte_budget"]
    cat_agg["pu_r"] = cat_agg["ca_reel"] / cat_agg["qte_reelle"]
    cat_agg["cu_b"] = cat_agg["cogs_budget"] / cat_agg["qte_budget"]
    cat_agg["cu_r"] = cat_agg["cogs_reel"] / cat_agg["qte_reelle"]

    cat_agg["ecart_ca_vol"] = (cat_agg["qte_reelle"] - cat_agg["qte_budget"]) * cat_agg["pu_b"]
    cat_agg["ecart_ca_prix"] = (cat_agg["pu_r"] - cat_agg["pu_b"]) * cat_agg["qte_reelle"]
    
    cat_agg["ecart_marge_qte"] = (cat_agg["qte_reelle"] - cat_agg["qte_budget"]) * (cat_agg["pu_b"] - cat_agg["cu_b"])
    cat_agg["ecart_marge_prix_vente"] = (cat_agg["pu_r"] - cat_agg["pu_b"]) * cat_agg["qte_reelle"]
    cat_agg["ecart_marge_cost_achat"] = - (cat_agg["cu_r"] - cat_agg["cu_b"]) * cat_agg["qte_reelle"]
    cat_agg["ecart_marge_total"] = cat_agg["marge_brute_reel"] - cat_agg["marge_brute_budget"]

    # Graphique en barres des écarts de marge
    fig_ecarts = px.bar(
        cat_agg,
        x="categorie",
        y=["ecart_marge_qte", "ecart_marge_prix_vente", "ecart_marge_cost_achat"],
        title="Décomposition de l'Écart de Marge par Catégorie (€)",
        barmode="group",
        labels={"value": "Écart (€)", "variable": "Composante d'Écart"}
    )
    st.plotly_chart(fig_ecarts, use_container_width=True)

    # Tableau récapitulatif
    st.markdown("#### Tableau Détaillé des Écarts de Marge (€)")
    st.dataframe(
        cat_agg[["categorie", "marge_brute_budget", "marge_brute_reel", "ecart_marge_total", "ecart_marge_qte", "ecart_marge_prix_vente", "ecart_marge_cost_achat"]].style.format({
            "marge_brute_budget": "{:,.0f} €", "marge_brute_reel": "{:,.0f} €",
            "ecart_marge_total": "{:,.0f} €", "ecart_marge_qte": "{:,.0f} €",
            "ecart_marge_prix_vente": "{:,.0f} €", "ecart_marge_cost_achat": "{:,.0f} €"
        }),
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# TAB 3 : COMPTE DE RÉSULTAT ANALYTIQUE
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("📑 Compte de Résultat Analytique par Catégorie")
    
    pnl_df = df_filtered.groupby("categorie").agg({
        "ca_reel": "sum",
        "cogs_reel": "sum",
        "marge_brute_reel": "sum",
        "couts_variables_autres": "sum",
        "couts_fixes_affectes": "sum"
    }).reset_index()

    pnl_df["mcv"] = pnl_df["marge_brute_reel"] - pnl_df["couts_variables_autres"]
    pnl_df["taux_mcv"] = (pnl_df["mcv"] / pnl_df["ca_reel"]) * 100
    pnl_df["resultat_analytique"] = pnl_df["mcv"] - pnl_df["couts_fixes_affectes"]
    pnl_df["seuil_rentabilite"] = pnl_df["couts_fixes_affectes"] / (pnl_df["taux_mcv"] / 100)
    pnl_df["point_mort_jours"] = ((pnl_df["seuil_rentabilite"] / pnl_df["ca_reel"]) * 365).round()

    st.dataframe(
        pnl_df.style.format({
            "ca_reel": "{:,.0f} €", "cogs_reel": "{:,.0f} €", "marge_brute_reel": "{:,.0f} €",
            "couts_variables_autres": "{:,.0f} €", "mcv": "{:,.0f} €", "taux_mcv": "{:.1f} %",
            "couts_fixes_affectes": "{:,.0f} €", "resultat_analytique": "{:,.0f} €",
            "seuil_rentabilite": "{:,.0f} €", "point_mort_jours": "{:.0f} Jours"
        }),
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# TAB 4 : STOCK, BFR & ROLLING FORECAST
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("💼 Métriques de Stock, BFR & Simulation d'Atterrissage")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 📦 Performance Stock & Cash")
        stock_moyen = df_filtered[["stock_debut", "stock_fin"]].mean(axis=1).sum()
        cogs_tot = df_filtered["cogs_reel"].sum()
        rot_stock = cogs_tot / stock_moyen if stock_moyen > 0 else 0
        duree_stock = 365 / rot_stock if rot_stock > 0 else 0
        cout_possession = stock_moyen * 0.20

        st.metric("Stock Moyen Valorisé", f"{stock_moyen:,.0f} €")
        st.metric("Rotation du Stock", f"{rot_stock:.2f} fois / an", f"{duree_stock:.0f} jours de stock")
        st.metric("Coût de Possession (20%/an)", f"{cout_possession:,.0f} €")

    with col_b:
        st.markdown("#### 🎯 Simulation Rolling Forecast (Fin d'Année)")
        budget_annuel = df["ca_budget"].sum()
        ca_8m = df[df["periode"] <= "2025-08"]["ca_reel"].sum()
        budget_8m = df[df["periode"] <= "2025-08"]["ca_budget"].sum()
        budget_4m = df[df["periode"] > "2025-08"]["ca_budget"].sum()
        
        taux_real_8m = ca_8m / budget_8m
        scen_a = ca_8m + (budget_4m * taux_real_8m)
        scen_b = ca_8m + budget_4m

        st.metric("Scénario A (Tendanciel à date)", f"{scen_a:,.0f} €", f"{(scen_a - budget_annuel):+,.0f} € vs Budget")
        st.metric("Scénario B (Plan de Redressement)", f"{scen_b:,.0f} €", f"{(scen_b - budget_annuel):+,.0f} € vs Budget")

# -----------------------------------------------------------------------------
# TAB 5 : COMMENTAIRE DE GESTION
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("📝 Commentaire de Gestion — Note de Synthèse CFO-Ready")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    comment_path = os.path.join(base_dir, "commentaire_de_gestion_mensuel.md")
    
    if os.path.exists(comment_path):
        with open(comment_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.info("Le fichier commentaire_de_gestion_mensuel.md est en cours de chargement.")
