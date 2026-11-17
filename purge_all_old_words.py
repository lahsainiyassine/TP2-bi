import os, re

process_dir = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\TP2_BI_VENTES\process"

# 1. Job_Dim_Client_Ventes
f1 = os.path.join(process_dir, "Job_Dim_Client_Ventes_0.1.item")
with open(f1, 'r', encoding='utf-8') as fp:
    c = fp.read()
c = c.replace("out_filiere", "out_client")
c = c.replace("Filieres", "Clients")
c = c.replace("xl_filieres", "clients_base")
with open(f1, 'w', encoding='utf-8') as fp:
    fp.write(c)

# 2. Job_Dim_Produit_Ventes
f2 = os.path.join(process_dir, "Job_Dim_Produit_Ventes_0.1.item")
with open(f2, 'r', encoding='utf-8') as fp:
    c = fp.read()
c = c.replace("out_filiere", "out_produit")
c = c.replace("Filieres", "Produits")
c = c.replace("nom_produit_filiere", "nom_produit")
c = c.replace("id_filiere", "id_produit_sk")
c = c.replace("xl_filieres", "produits_catalogue")
with open(f2, 'w', encoding='utf-8') as fp:
    fp.write(c)

# 3. Job_Dim_Magasin_Ventes
f3 = os.path.join(process_dir, "Job_Dim_Magasin_Ventes_0.1.item")
with open(f3, 'r', encoding='utf-8') as fp:
    c = fp.read()
c = c.replace("out_filiere", "out_magasin")
c = c.replace("Filieres", "Magasins")
c = c.replace("nom_magasin_filiere", "nom_magasin")
c = c.replace("id_filiere", "id_magasin_sk")
c = c.replace("xl_filieres", "magasins_ventes")
with open(f3, 'w', encoding='utf-8') as fp:
    fp.write(c)

# 4. Job_Dim_Temps_Ventes
f4 = os.path.join(process_dir, "Job_Dim_Temps_Ventes_0.1.item")
with open(f4, 'r', encoding='utf-8') as fp:
    c = fp.read()
c = c.replace("Inscriptions_2024", "ventes_synthese")
c = c.replace("Inscriptions", "ventes_synthese")
c = c.replace("id_inscription", "id_vente")
c = c.replace("id_etudiant", "id_client_fk")
c = c.replace("id_filiere", "id_produit_fk")
c = c.replace("statut", "mode_paiement")
with open(f4, 'w', encoding='utf-8') as fp:
    fp.write(c)

# 5. Job_Fait_Ventes
f5 = os.path.join(process_dir, "Job_Fait_Ventes_0.1.item")
with open(f5, 'r', encoding='utf-8') as fp:
    c = fp.read()
c = c.replace("Inscriptions_2024", "ventes_synthese")
c = c.replace("Inscriptions", "ventes_synthese")
c = c.replace("id_inscription", "code_vente")
c = c.replace("nom_filiere", "nom_produit")
c = c.replace("statut", "mode_paiement")
c = c.replace("date_inscription", "date_vente")
c = c.replace("out_fait", "out_ventes")
with open(f5, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("Purge completed! Verified:")
