import os, csv, zipfile, datetime
import xml.etree.ElementTree as ET

base_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\Etude de cas DW Fichiers Sources\Etude de cas DW"
out_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\donnees_transformees"
os.makedirs(out_dir, exist_ok=True)

def excel_date_to_datetime(val):
    try:
        n = float(val)
        return datetime.datetime(1899, 12, 30) + datetime.timedelta(days=n)
    except:
        try:
            return datetime.datetime.strptime(str(val).strip(), '%Y-%m-%d')
        except:
            return None

def read_xlsx(path):
    with zipfile.ZipFile(path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            for si in tree.findall('ns:si', ns):
                t = si.find('ns:t', ns)
                if t is not None and t.text:
                    shared_strings.append(t.text)
                else:
                    texts = [elem.text for elem in si.iter() if elem.text]
                    shared_strings.append("".join(texts))
        sheet_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        ns_s = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        rows = []
        for row in sheet_tree.findall('.//ns:row', ns_s):
            cols = {}
            for c in row.findall('ns:c', ns_s):
                ref = c.attrib.get('r')
                col_letter = "".join([ch for ch in ref if ch.isalpha()])
                t = c.attrib.get('t')
                v = c.find('ns:v', ns_s)
                val = v.text if v is not None else None
                if val is not None and t == 's':
                    val = shared_strings[int(val)]
                cols[col_letter] = val
            rows.append(cols)
        h_keys = sorted(rows[0].keys())
        data = []
        for r in rows[1:]:
            data.append({rows[0][k]: r.get(k) for k in h_keys})
        return data

# 1. GENERATE DIM_TEMPS
print("Generating dim_temps...")
dates_set = set()

# from clients_base
c_base = read_xlsx(os.path.join(base_dir, 'clients_base_50.xlsx'))
for r in c_base:
    dt = excel_date_to_datetime(r.get('date_inscription'))
    if dt: dates_set.add(dt.date())

# from clients_online
with open(os.path.join(base_dir, 'clients_online_50.csv'), 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        dt = excel_date_to_datetime(r.get('first_purchase_date'))
        if dt: dates_set.add(dt.date())

# from produits
p_cat = read_xlsx(os.path.join(base_dir, 'produits_catalogue.xlsx'))
for r in p_cat:
    dt = excel_date_to_datetime(r.get('date_insertion'))
    if dt: dates_set.add(dt.date())

# from magasins
with open(os.path.join(base_dir, 'magasins_localisation (2).csv'), 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        dt = excel_date_to_datetime(r.get('date_ouverture'))
        if dt: dates_set.add(dt.date())

# from ventes
v_syn = read_xlsx(os.path.join(base_dir, 'ventes_synthese.xlsx'))
for r in v_syn:
    dt = excel_date_to_datetime(r.get('date_vente'))
    if dt: dates_set.add(dt.date())

mois_fr = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

dim_temps_rows = []
for d in sorted(dates_set):
    id_temps = int(d.strftime('%Y%m%d'))
    trimestre = (d.month - 1) // 3 + 1
    dim_temps_rows.append({
        'id_temps': id_temps,
        'date_complete': d.strftime('%Y-%m-%d'),
        'jour': d.day,
        'mois': d.month,
        'nom_mois': mois_fr[d.month],
        'trimestre': trimestre,
        'annee': d.year,
        'jour_semaine': jours_fr[d.weekday()]
    })

temps_csv = os.path.join(out_dir, 'dim_temps.csv')
with open(temps_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(dim_temps_rows[0].keys()))
    w.writeheader()
    w.writerows(dim_temps_rows)
print(f"dim_temps written: {len(dim_temps_rows)} records")

# 2. GENERATE DIM_CLIENT
print("Generating dim_client...")
with open(os.path.join(base_dir, 'clients_online_50.csv'), 'r', encoding='utf-8') as f:
    c_online_dict = {r['client_code']: r for r in csv.DictReader(f)}
tree = ET.parse(os.path.join(base_dir, 'clients_fidelite_50.xml'))
c_fid_dict = {el.find('id').text: {'points': el.find('points').text, 'carte': el.find('carte').text} for el in tree.getroot()}

dim_client_rows = [{
    'id_client_sk': 1,
    'code_client': 'C_INCONNU',
    'nom': 'Inconnu',
    'prenom': 'Inconnu',
    'nom_complet': 'Client Inconnu',
    'ville': 'Non spécifiée',
    'email': 'inconnu@entreprise.com',
    'segment_marketing': 'Standard',
    'date_inscription': '2000-01-01',
    'points_fidelite': 0,
    'type_carte': 'Standard'
}]

for idx, cb in enumerate(c_base, start=2):
    cid = cb['client_id']
    co = c_online_dict.get(cid, {})
    cf = c_fid_dict.get(cid, {})
    dt = excel_date_to_datetime(cb.get('date_inscription'))
    dt_str = dt.strftime('%Y-%m-%d') if dt else '2000-01-01'
    
    full_name = co.get('full_name') if co.get('full_name') else f"{cb.get('prenom')} {cb.get('nom')}".strip()
    dim_client_rows.append({
        'id_client_sk': idx,
        'code_client': cid,
        'nom': cb.get('nom'),
        'prenom': cb.get('prenom'),
        'nom_complet': full_name,
        'ville': cb.get('ville'),
        'email': cb.get('email'),
        'segment_marketing': cb.get('segment_marketing'),
        'date_inscription': dt_str,
        'points_fidelite': int(cf.get('points', 0)),
        'type_carte': cf.get('carte', 'Standard')
    })

client_csv = os.path.join(out_dir, 'dim_client.csv')
with open(client_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(dim_client_rows[0].keys()))
    w.writeheader()
    w.writerows(dim_client_rows)
print(f"dim_client written: {len(dim_client_rows)} records")

# 3. GENERATE DIM_PRODUIT
print("Generating dim_produit...")
with open(os.path.join(base_dir, 'produits_fournisseurs.csv'), 'r', encoding='utf-8') as f:
    p_four_dict = {r['code_produit']: r for r in csv.DictReader(f)}

dim_produit_rows = [{
    'id_produit_sk': 1,
    'code_produit': 'P_INCONNU',
    'nom_produit': 'Produit Inconnu',
    'categorie': 'Non catégorisé',
    'sous_categorie': 'Non catégorisé',
    'marque': 'Générique',
    'prix_achat': 0.00,
    'prix_vente': 0.00,
    'fournisseur': 'Inconnu',
    'pays_fournisseur': 'Inconnu',
    'delai_livraison_jours': 0,
    'cout_transport': 0.00,
    'statut': 'Inactif'
}]

for idx, p in enumerate(p_cat, start=2):
    pid = p['code_produit']
    pf = p_four_dict.get(pid, {})
    dim_produit_rows.append({
        'id_produit_sk': idx,
        'code_produit': pid,
        'nom_produit': p.get('nom_produit'),
        'categorie': p.get('catégorie'),
        'sous_categorie': p.get('sous_catégorie'),
        'marque': p.get('marque'),
        'prix_achat': round(float(p.get('prix_achat', 0)), 2),
        'prix_vente': round(float(p.get('prix_vente', 0)), 2),
        'fournisseur': pf.get('fournisseur', 'Inconnu'),
        'pays_fournisseur': pf.get('pays_fournisseur', 'Inconnu'),
        'delai_livraison_jours': int(pf.get('delai_livraison_jours', 0)),
        'cout_transport': round(float(pf.get('coût_transport', 0)), 2),
        'statut': p.get('statut')
    })

produit_csv = os.path.join(out_dir, 'dim_produit.csv')
with open(produit_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(dim_produit_rows[0].keys()))
    w.writeheader()
    w.writerows(dim_produit_rows)
print(f"dim_produit written: {len(dim_produit_rows)} records")

# 4. GENERATE DIM_MAGASIN
print("Generating dim_magasin...")
m_ven = read_xlsx(os.path.join(base_dir, 'magasins_ventes (1).xlsx'))
m_ven_dict = {r['code_magasin']: r for r in m_ven}

dim_magasin_rows = [{
    'id_magasin_sk': 1,
    'code_magasin': 'M_INCONNU',
    'nom_magasin': 'Magasin Inconnu',
    'ville': 'Non spécifiée',
    'region': 'Non spécifiée',
    'pays': 'Maroc',
    'surface_m2': 0,
    'type_magasin': 'Inconnu',
    'date_ouverture': '2000-01-01',
    'responsable_magasin': 'Inconnu',
    'nb_employes': 0,
    'chiffre_affaires_annuel': 0.00,
    'frais_fonctionnement': 0.00,
    'statut': 'Inactif'
}]

with open(os.path.join(base_dir, 'magasins_localisation (2).csv'), 'r', encoding='utf-8') as f:
    for idx, ml in enumerate(csv.DictReader(f), start=2):
        mid = ml['code_magasin']
        mv = m_ven_dict.get(mid, {})
        dim_magasin_rows.append({
            'id_magasin_sk': idx,
            'code_magasin': mid,
            'nom_magasin': ml.get('nom_magasin'),
            'ville': ml.get('ville'),
            'region': ml.get('région'),
            'pays': ml.get('pays'),
            'surface_m2': int(ml.get('surface_m2', 0)),
            'type_magasin': ml.get('type_magasin'),
            'date_ouverture': ml.get('date_ouverture'),
            'responsable_magasin': mv.get('responsable_magasin'),
            'nb_employes': int(mv.get('nb_employes', 0)),
            'chiffre_affaires_annuel': round(float(mv.get('chiffre_affaires_annuel', 0)), 2),
            'frais_fonctionnement': round(float(mv.get('frais_fonctionnement', 0)), 2),
            'statut': mv.get('statut')
        })

magasin_csv = os.path.join(out_dir, 'dim_magasin.csv')
with open(magasin_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(dim_magasin_rows[0].keys()))
    w.writeheader()
    w.writerows(dim_magasin_rows)
print(f"dim_magasin written: {len(dim_magasin_rows)} records")

# 5. GENERATE FAIT_VENTES
print("Generating fait_ventes...")
client_map = {r['code_client']: r['id_client_sk'] for r in dim_client_rows}
produit_map = {r['code_produit']: r['id_produit_sk'] for r in dim_produit_rows}
magasin_map = {r['code_magasin']: r['id_magasin_sk'] for r in dim_magasin_rows}

fait_ventes_rows = []
for idx, v in enumerate(v_syn, start=1):
    c_src = v.get('id_client_source')
    p_src = v.get('id_produit_source')
    m_src = v.get('id_magasin_source')
    
    # lookup or default unknown (id=1)
    c_fk = client_map.get(c_src, 1)
    p_fk = produit_map.get(p_src, 1)
    m_fk = magasin_map.get(m_src, 1)
    
    dt = excel_date_to_datetime(v.get('date_vente'))
    t_fk = int(dt.strftime('%Y%m%d')) if dt else 20000101
    
    q = int(float(v.get('quantite_vendue', 0)))
    pu = round(float(v.get('prix_unitaire', 0)), 2)
    mt = round(q * pu, 2)
    
    fait_ventes_rows.append({
        'id_vente_sk': idx,
        'code_vente': v.get('id_vente'),
        'id_client_fk': c_fk,
        'id_produit_fk': p_fk,
        'id_magasin_fk': m_fk,
        'id_temps_fk': t_fk,
        'quantite_vendue': q,
        'prix_unitaire': pu,
        'montant_total': mt,
        'mode_paiement': v.get('mode_paiement')
    })

ventes_csv = os.path.join(out_dir, 'fait_ventes.csv')
with open(ventes_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(fait_ventes_rows[0].keys()))
    w.writeheader()
    w.writerows(fait_ventes_rows)
print(f"fait_ventes written: {len(fait_ventes_rows)} records")
