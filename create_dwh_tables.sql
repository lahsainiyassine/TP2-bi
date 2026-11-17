-- =====================================================================
-- SCRIPT DE CRÉATION DU DATA WAREHOUSE - MINI PROJET BI
-- Université Cadi Ayyad - ENS Marrakech
-- Master TEE - Semestre 3 - Pr. Oumaima STITINI
-- =====================================================================

DROP DATABASE IF EXISTS dwh_ventes;
CREATE DATABASE dwh_ventes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dwh_ventes;

-- ---------------------------------------------------------------------
-- 1. TABLE DE DIMENSION : dim_temps
-- ---------------------------------------------------------------------
CREATE TABLE dim_temps (
    id_temps INT PRIMARY KEY,                       -- Format YYYYMMDD (ex: 20230325)
    date_complete DATE NOT NULL UNIQUE,             -- Date complète (YYYY-MM-DD)
    jour INT NOT NULL,                              -- 1 à 31
    mois INT NOT NULL,                              -- 1 à 12
    nom_mois VARCHAR(20) NOT NULL,                  -- Janvier, Février...
    trimestre INT NOT NULL,                         -- 1, 2, 3, 4
    annee INT NOT NULL,                             -- 2005 à 2025
    jour_semaine VARCHAR(20) NOT NULL               -- Lundi, Mardi...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- 2. TABLE DE DIMENSION : dim_client
-- ---------------------------------------------------------------------
CREATE TABLE dim_client (
    id_client_sk INT AUTO_INCREMENT PRIMARY KEY,    -- Clé de substitution (Surrogate Key)
    code_client VARCHAR(20) NOT NULL UNIQUE,        -- Identifiant source (ex: C001, C002...)
    nom VARCHAR(100),
    prenom VARCHAR(100),
    nom_complet VARCHAR(200),
    ville VARCHAR(100),
    email VARCHAR(150),
    segment_marketing VARCHAR(50),                  -- VIP, Premium, Standard
    date_inscription DATE,
    points_fidelite INT DEFAULT 0,
    type_carte VARCHAR(50)                          -- Gold, Silver, Platinum...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertion de la ligne par défaut pour gérer les clients inconnus (intégrité référentielle)
INSERT INTO dim_client (id_client_sk, code_client, nom, prenom, nom_complet, ville, email, segment_marketing, date_inscription, points_fidelite, type_carte)
VALUES (1, 'C_INCONNU', 'Inconnu', 'Inconnu', 'Client Inconnu', 'Non spécifiée', 'inconnu@entreprise.com', 'Standard', '2000-01-01', 0, 'Standard');

-- ---------------------------------------------------------------------
-- 3. TABLE DE DIMENSION : dim_produit
-- ---------------------------------------------------------------------
CREATE TABLE dim_produit (
    id_produit_sk INT AUTO_INCREMENT PRIMARY KEY,   -- Clé de substitution (Surrogate Key)
    code_produit VARCHAR(20) NOT NULL UNIQUE,       -- Identifiant source (ex: P001, P002...)
    nom_produit VARCHAR(150),
    categorie VARCHAR(100),
    sous_categorie VARCHAR(100),
    marque VARCHAR(100),
    prix_achat DECIMAL(10,2),
    prix_vente DECIMAL(10,2),
    fournisseur VARCHAR(100),
    pays_fournisseur VARCHAR(100),
    delai_livraison_jours INT,
    cout_transport DECIMAL(10,2),
    statut VARCHAR(50)                              -- Actif, Inactif
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertion de la ligne par défaut pour gérer les produits inconnus
INSERT INTO dim_produit (id_produit_sk, code_produit, nom_produit, categorie, sous_categorie, marque, prix_achat, prix_vente, fournisseur, pays_fournisseur, delai_livraison_jours, cout_transport, statut)
VALUES (1, 'P_INCONNU', 'Produit Inconnu', 'Non catégorisé', 'Non catégorisé', 'Générique', 0.00, 0.00, 'Inconnu', 'Inconnu', 0, 0.00, 'Inactif');

-- ---------------------------------------------------------------------
-- 4. TABLE DE DIMENSION : dim_magasin
-- ---------------------------------------------------------------------
CREATE TABLE dim_magasin (
    id_magasin_sk INT AUTO_INCREMENT PRIMARY KEY,   -- Clé de substitution (Surrogate Key)
    code_magasin VARCHAR(20) NOT NULL UNIQUE,       -- Identifiant source (ex: M001, M002...)
    nom_magasin VARCHAR(150),
    ville VARCHAR(100),
    region VARCHAR(100),
    pays VARCHAR(100),
    surface_m2 INT,
    type_magasin VARCHAR(50),                       -- Supermarché, Hypermarché...
    date_ouverture DATE,
    responsable_magasin VARCHAR(150),
    nb_employes INT,
    chiffre_affaires_annuel DECIMAL(15,2),
    frais_fonctionnement DECIMAL(15,2),
    statut VARCHAR(50)                              -- Actif, Inactif
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertion de la ligne par défaut pour les magasins
INSERT INTO dim_magasin (id_magasin_sk, code_magasin, nom_magasin, ville, region, pays, surface_m2, type_magasin, date_ouverture, responsable_magasin, nb_employes, chiffre_affaires_annuel, frais_fonctionnement, statut)
VALUES (1, 'M_INCONNU', 'Magasin Inconnu', 'Non spécifiée', 'Non spécifiée', 'Maroc', 0, 'Inconnu', '2000-01-01', 'Inconnu', 0, 0.00, 0.00, 'Inactif');

-- ---------------------------------------------------------------------
-- 5. TABLE DE FAITS : fait_ventes
-- ---------------------------------------------------------------------
CREATE TABLE fait_ventes (
    id_vente_sk INT AUTO_INCREMENT PRIMARY KEY,     -- Clé de fait auto-incrémentée
    code_vente VARCHAR(20) NOT NULL UNIQUE,         -- Code transaction (V001, V002...)
    id_client_fk INT NOT NULL,                      -- Clé étrangère vers dim_client
    id_produit_fk INT NOT NULL,                     -- Clé étrangère vers dim_produit
    id_magasin_fk INT NOT NULL,                     -- Clé étrangère vers dim_magasin
    id_temps_fk INT NOT NULL,                       -- Clé étrangère vers dim_temps
    quantite_vendue INT NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    montant_total DECIMAL(12,2) NOT NULL,           -- quantite_vendue * prix_unitaire
    mode_paiement VARCHAR(50),
    
    -- Contraintes d'intégrité référentielle
    CONSTRAINT fk_ventes_client FOREIGN KEY (id_client_fk) REFERENCES dim_client(id_client_sk),
    CONSTRAINT fk_ventes_produit FOREIGN KEY (id_produit_fk) REFERENCES dim_produit(id_produit_sk),
    CONSTRAINT fk_ventes_magasin FOREIGN KEY (id_magasin_fk) REFERENCES dim_magasin(id_magasin_sk),
    CONSTRAINT fk_ventes_temps FOREIGN KEY (id_temps_fk) REFERENCES dim_temps(id_temps)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
