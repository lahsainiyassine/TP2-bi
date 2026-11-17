import os, re

tp2_process_dir = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\TP2_BI_VENTES\process"
sources_dir = r"C:/Users/pc/OneDrive/Bureau/ETL/Etude de cas DW Fichiers Sources/Etude de cas DW"

# 1. Clean Job_Dim_Client_Ventes
client_file = os.path.join(tp2_process_dir, "Job_Dim_Client_Ventes_0.1.item")
with open(client_file, 'r', encoding='utf-8') as f:
    c = f.read()
# Replace any leftover filiere/etudiant
c = c.replace("dim_filiere", "dim_client")
c = c.replace("id_filiere", "id_client_sk")
c = c.replace("nom_filiere", "nom")
c = c.replace("Filieres.xlsx", "clients_base_50.xlsx")
c = c.replace("xl_filieres", "xl_clients")
c = c.replace('"filiere"', '"client"')
with open(client_file, 'w', encoding='utf-8') as f:
    f.write(c)

# 2. Clean Job_Dim_Produit_Ventes
produit_file = os.path.join(tp2_process_dir, "Job_Dim_Produit_Ventes_0.1.item")
with open(produit_file, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("dim_client", "dim_produit")
c = c.replace("id_client_sk", "id_produit_sk")
c = c.replace("nom", "nom_produit")
c = c.replace("clients_base_50.xlsx", "produits_catalogue.xlsx")
c = c.replace("xl_clients", "xl_produits")
with open(produit_file, 'w', encoding='utf-8') as f:
    f.write(c)

# 3. Clean Job_Dim_Magasin_Ventes
magasin_file = os.path.join(tp2_process_dir, "Job_Dim_Magasin_Ventes_0.1.item")
with open(magasin_file, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("dim_client", "dim_magasin")
c = c.replace("id_client_sk", "id_magasin_sk")
c = c.replace("nom", "nom_magasin")
c = c.replace("clients_base_50.xlsx", "magasins_ventes (1).xlsx")
c = c.replace("xl_clients", "xl_magasins")
with open(magasin_file, 'w', encoding='utf-8') as f:
    f.write(c)

# 4. Clean Job_Dim_Temps_Ventes
temps_file = os.path.join(tp2_process_dir, "Job_Dim_Temps_Ventes_0.1.item")
with open(temps_file, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("Inscriptions.xlsx", "ventes_synthese.xlsx")
c = c.replace("xl_inscriptions", "xl_ventes_temps")
c = c.replace("date_inscription", "date_vente")
with open(temps_file, 'w', encoding='utf-8') as f:
    f.write(c)

# 5. Clean Job_Fait_Ventes
fait_file = os.path.join(tp2_process_dir, "Job_Fait_Ventes_0.1.item")
with open(fait_file, 'r', encoding='utf-8') as f:
    c = f.read()
# Replace old labels and tables completely
c = c.replace("xl_inscriptions", "xl_ventes")
c = c.replace("Inscriptions.xlsx", "ventes_synthese.xlsx")
c = c.replace('"dim_filiere"', '"dim_client"')
c = c.replace('"dim_etudiant"', '"dim_produit"')
c = c.replace('"dim_statut"', '"dim_magasin"')
c = c.replace('"dim_geo"', '"dim_magasin"')
c = c.replace("dim_filiere", "dim_client")
c = c.replace("dim_etudiant", "dim_produit")
c = c.replace("id_filiere", "id_client_fk")
c = c.replace("id_etudiant", "id_produit_fk")
c = c.replace("id_statut", "id_magasin_fk")
c = c.replace("id_geo", "id_magasin_fk")
c = c.replace("montant_paye", "montant_total")
c = c.replace("nb_inscriptions", "quantite_vendue")

with open(fait_file, 'w', encoding='utf-8') as f:
    f.write(c)

print("All 5 job files in TP2_BI_VENTES have been completely cleaned and purged of any old TP references!")
