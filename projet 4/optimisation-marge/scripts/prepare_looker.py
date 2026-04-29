import pandas as pd
import os

def prepare_looker_data():
    print("Début de la préparation des données pour Looker...")
    
    # Chemins des fichiers
    base_path = "data"
    orders_path = os.path.join(base_path, "olist_orders_dataset.csv")
    items_path = os.path.join(base_path, "olist_order_items_dataset.csv")
    products_path = os.path.join(base_path, "olist_products_dataset.csv")
    sellers_path = os.path.join(base_path, "olist_sellers_dataset.csv")
    
    # 1. Chargement des données
    print("Chargement des fichiers CSV...")
    orders = pd.read_csv(orders_path)
    items = pd.read_csv(items_path)
    products = pd.read_csv(products_path)
    sellers = pd.read_csv(sellers_path)
    
    # 2. Jointures
    print("Exécution des jointures...")
    # Jointure Items + Orders
    df = pd.merge(items, orders, on="order_id", how="inner")
    
    # Jointure avec Products
    df = pd.merge(df, products, on="product_id", how="left")
    
    # Jointure avec Sellers
    df = pd.merge(df, sellers, on="seller_id", how="left")
    
    # 3. Sélection des colonnes finales
    final_columns = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "product_category_name",
        "price",
        "seller_id",
        "seller_state"
    ]
    
    df_looker = df[final_columns]
    
    # 4. Exportation
    output_path = os.path.join(base_path, "olist_looker.csv")
    print(f"Exportation du résultat vers {output_path}...")
    df_looker.to_csv(output_path, index=False)
    
    print("Préparation terminée avec succès !")
    print(f"Dimensions finales : {df_looker.shape}")

if __name__ == "__main__":
    prepare_looker_data()
