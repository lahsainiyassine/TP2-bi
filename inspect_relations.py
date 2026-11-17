import os, csv, zipfile, datetime
import xml.etree.ElementTree as ET

base_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\Etude de cas DW Fichiers Sources\Etude de cas DW"

def excel_date_to_str(val):
    try:
        n = float(val)
        # Excel date epoch: 1899-12-30
        d = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=n)
        return d.strftime('%Y-%m-%d')
    except:
        return val

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
        
        # normalize to list of lists using header keys
        header_keys = sorted(rows[0].keys())
        headers = [rows[0][k] for k in header_keys]
        data = []
        for r in rows[1:]:
            data.append([r.get(k) for k in header_keys])
        return headers, data

# Check Clients
h_c_base, d_c_base = read_xlsx(os.path.join(base_dir, 'clients_base_50.xlsx'))
print("=== CLIENTS BASE ===")
print("Headers:", h_c_base)
ids_c_base = [r[0] for r in d_c_base]
print(f"Count: {len(ids_c_base)}, Min ID: {min(ids_c_base)}, Max ID: {max(ids_c_base)}")

# XML clients fidelite
tree = ET.parse(os.path.join(base_dir, 'clients_fidelite_50.xml'))
root = tree.getroot()
fidelite = []
for c in root:
    fidelite.append({el.tag: el.text for el in c})
print("\n=== CLIENTS FIDELITE (XML) ===")
print(f"Count: {len(fidelite)}")
ids_c_fid = [f.get('id') for f in fidelite]
print(f"Min ID: {min(ids_c_fid)}, Max ID: {max(ids_c_fid)}")

# CSV clients online
with open(os.path.join(base_dir, 'clients_online_50.csv'), 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    h_c_on = next(r)
    d_c_on = list(r)
print("\n=== CLIENTS ONLINE (CSV) ===")
print("Headers:", h_c_on)
ids_c_on = [row[0] for row in d_c_on]
print(f"Count: {len(ids_c_on)}, Min ID: {min(ids_c_on)}, Max ID: {max(ids_c_on)}")

# Compare Client IDs
print("\nClient ID overlap:")
print("Base vs Fid:", len(set(ids_c_base).intersection(ids_c_fid)))
print("Base vs Online:", len(set(ids_c_base).intersection(ids_c_on)))
print("Fid vs Online:", len(set(ids_c_fid).intersection(ids_c_on)))

# Check Magasins
with open(os.path.join(base_dir, 'magasins_localisation (2).csv'), 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    h_m_loc = next(r)
    d_m_loc = list(r)
h_m_ven, d_m_ven = read_xlsx(os.path.join(base_dir, 'magasins_ventes (1).xlsx'))
ids_m_loc = [row[0] for row in d_m_loc]
ids_m_ven = [row[0] for row in d_m_ven]
print("\n=== MAGASINS ===")
print(f"Loc count: {len(ids_m_loc)}, Ventes count: {len(ids_m_ven)}")
print("Overlap:", len(set(ids_m_loc).intersection(ids_m_ven)))

# Check Produits
h_p_cat, d_p_cat = read_xlsx(os.path.join(base_dir, 'produits_catalogue.xlsx'))
with open(os.path.join(base_dir, 'produits_fournisseurs.csv'), 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    h_p_four = next(r)
    d_p_four = list(r)
ids_p_cat = [row[0] for row in d_p_cat]
ids_p_four = [row[0] for row in d_p_four]
print("\n=== PRODUITS ===")
print(f"Cat count: {len(ids_p_cat)}, Four count: {len(ids_p_four)}")
print("Overlap:", len(set(ids_p_cat).intersection(ids_p_four)))

# Check Ventes
h_v, d_v = read_xlsx(os.path.join(base_dir, 'ventes_synthese.xlsx'))
print("\n=== VENTES ===")
print("Headers:", h_v)
print(f"Count: {len(d_v)}")
v_c_ids = [row[1] for row in d_v]
v_p_ids = [row[2] for row in d_v]
v_m_ids = [row[3] for row in d_v]
print("Unique clients in ventes:", len(set(v_c_ids)), "Range:", min(v_c_ids), "to", max(v_c_ids))
print("Clients in ventes in base:", len(set(v_c_ids).intersection(ids_c_base)))
print("Unique products in ventes:", len(set(v_p_ids)), "Range:", min(v_p_ids), "to", max(v_p_ids))
print("Products in ventes in cat:", len(set(v_p_ids).intersection(ids_p_cat)))
print("Unique magasins in ventes:", len(set(v_m_ids)), "Range:", min(v_m_ids), "to", max(v_m_ids))
print("Magasins in ventes in loc:", len(set(v_m_ids).intersection(ids_m_loc)))
