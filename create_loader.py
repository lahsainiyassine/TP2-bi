import csv
import subprocess

csv_dir = r"C:/Users/pc/OneDrive/Bureau/ETL/donnees_transformees"
mysql_exe = r"C:\xampp\mysql\bin\mysql.exe"

sql_commands = """
USE dwh_ventes;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE fait_ventes;
TRUNCATE TABLE dim_client;
TRUNCATE TABLE dim_produit;
TRUNCATE TABLE dim_magasin;
TRUNCATE TABLE dim_temps;
"""

# Load dim_temps
with open(csv_dir + "/dim_temps.csv", 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    vals = []
    for row in r:
        vals.append(f"({row['id_temps']}, '{row['date_complete']}', {row['jour']}, {row['mois']}, '{row['nom_mois']}', {row['trimestre']}, {row['annee']}, '{row['jour_semaine']}')")
    sql_commands += f"INSERT INTO dim_temps (id_temps, date_complete, jour, mois, nom_mois, trimestre, annee, jour_semaine) VALUES \n" + ",\n".join(vals) + ";\n"

# Load dim_client
with open(csv_dir + "/dim_client.csv", 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    vals = []
    for row in r:
        nom = row['nom'].replace("'", "''") if row['nom'] else ''
        prenom = row['prenom'].replace("'", "''") if row['prenom'] else ''
        nom_c = row['nom_complet'].replace("'", "''") if row['nom_complet'] else ''
        ville = row['ville'].replace("'", "''") if row['ville'] else ''
        email = row['email'].replace("'", "''") if row['email'] else ''
        seg = row['segment_marketing'].replace("'", "''") if row['segment_marketing'] else ''
        carte = row['type_carte'].replace("'", "''") if row['type_carte'] else ''
        vals.append(f"({row['id_client_sk']}, '{row['code_client']}', '{nom}', '{prenom}', '{nom_c}', '{ville}', '{email}', '{seg}', '{row['date_inscription']}', {row['points_fidelite']}, '{carte}')")
    sql_commands += f"INSERT INTO dim_client (id_client_sk, code_client, nom, prenom, nom_complet, ville, email, segment_marketing, date_inscription, points_fidelite, type_carte) VALUES \n" + ",\n".join(vals) + ";\n"

# Load dim_produit
with open(csv_dir + "/dim_produit.csv", 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    vals = []
    for row in r:
        nom = row['nom_produit'].replace("'", "''") if row['nom_produit'] else ''
        cat = row['categorie'].replace("'", "''") if row['categorie'] else ''
        scat = row['sous_categorie'].replace("'", "''") if row['sous_categorie'] else ''
        marque = row['marque'].replace("'", "''") if row['marque'] else ''
        four = row['fournisseur'].replace("'", "''") if row['fournisseur'] else ''
        pfour = row['pays_fournisseur'].replace("'", "''") if row['pays_fournisseur'] else ''
        stat = row['statut'].replace("'", "''") if row['statut'] else ''
        vals.append(f"({row['id_produit_sk']}, '{row['code_produit']}', '{nom}', '{cat}', '{scat}', '{marque}', {row['prix_achat']}, {row['prix_vente']}, '{four}', '{pfour}', {row['delai_livraison_jours']}, {row['cout_transport']}, '{stat}')")
    sql_commands += f"INSERT INTO dim_produit (id_produit_sk, code_produit, nom_produit, categorie, sous_categorie, marque, prix_achat, prix_vente, fournisseur, pays_fournisseur, delai_livraison_jours, cout_transport, statut) VALUES \n" + ",\n".join(vals) + ";\n"

# Load dim_magasin
with open(csv_dir + "/dim_magasin.csv", 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    vals = []
    for row in r:
        nom = row['nom_magasin'].replace("'", "''") if row['nom_magasin'] else ''
        ville = row['ville'].replace("'", "''") if row['ville'] else ''
        reg = row['region'].replace("'", "''") if row['region'] else ''
        pays = row['pays'].replace("'", "''") if row['pays'] else ''
        tmag = row['type_magasin'].replace("'", "''") if row['type_magasin'] else ''
        resp = row['responsable_magasin'].replace("'", "''") if row['responsable_magasin'] else ''
        stat = row['statut'].replace("'", "''") if row['statut'] else ''
        vals.append(f"({row['id_magasin_sk']}, '{row['code_magasin']}', '{nom}', '{ville}', '{reg}', '{pays}', {row['surface_m2']}, '{tmag}', '{row['date_ouverture']}', '{resp}', {row['nb_employes']}, {row['chiffre_affaires_annuel']}, {row['frais_fonctionnement']}, '{stat}')")
    sql_commands += f"INSERT INTO dim_magasin (id_magasin_sk, code_magasin, nom_magasin, ville, region, pays, surface_m2, type_magasin, date_ouverture, responsable_magasin, nb_employes, chiffre_affaires_annuel, frais_fonctionnement, statut) VALUES \n" + ",\n".join(vals) + ";\n"

# Load fait_ventes
with open(csv_dir + "/fait_ventes.csv", 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    vals = []
    for row in r:
        mp = row['mode_paiement'].replace("'", "''") if row['mode_paiement'] else ''
        vals.append(f"({row['id_vente_sk']}, '{row['code_vente']}', {row['id_client_fk']}, {row['id_produit_fk']}, {row['id_magasin_fk']}, {row['id_temps_fk']}, {row['quantite_vendue']}, {row['prix_unitaire']}, {row['montant_total']}, '{mp}')")
    sql_commands += f"INSERT INTO fait_ventes (id_vente_sk, code_vente, id_client_fk, id_produit_fk, id_magasin_fk, id_temps_fk, quantite_vendue, prix_unitaire, montant_total, mode_paiement) VALUES \n" + ",\n".join(vals) + ";\n"

sql_commands += "SET FOREIGN_KEY_CHECKS = 1;\n"

load_sql_file = r"C:\Users\pc\OneDrive\Bureau\ETL\load_data.sql"
with open(load_sql_file, 'w', encoding='utf-8') as f:
    f.write(sql_commands)

print("load_data.sql created successfully!")
