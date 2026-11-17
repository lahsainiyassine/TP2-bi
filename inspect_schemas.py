import os, csv, zipfile
import xml.etree.ElementTree as ET

base_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\Etude de cas DW Fichiers Sources\Etude de cas DW"

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
        headers = [rows[0][k] for k in h_keys]
        data = []
        for r in rows[1:]:
            data.append({rows[0][k]: r.get(k) for k in h_keys})
        return headers, data

print("=== 1. CLIENTS ===")
h, d = read_xlsx(os.path.join(base_dir, 'clients_base_50.xlsx'))
print("clients_base_50.xlsx columns:", h)
print("sample row 1:", d[0])

with open(os.path.join(base_dir, 'clients_online_50.csv'), 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    print("clients_online_50.csv columns:", r.fieldnames)
    d_csv = list(r)
    print("sample row 1:", d_csv[0])

tree = ET.parse(os.path.join(base_dir, 'clients_fidelite_50.xml'))
d_xml = [{el.tag: el.text for el in c} for c in tree.getroot()]
print("clients_fidelite_50.xml tags:", list(d_xml[0].keys()))
print("sample row 1:", d_xml[0])

print("\n=== 2. MAGASINS ===")
with open(os.path.join(base_dir, 'magasins_localisation (2).csv'), 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    print("magasins_localisation.csv columns:", r.fieldnames)
    d_m_loc = list(r)
    print("sample row 1:", d_m_loc[0])

h, d_m_ven = read_xlsx(os.path.join(base_dir, 'magasins_ventes (1).xlsx'))
print("magasins_ventes.xlsx columns:", h)
print("sample row 1:", d_m_ven[0])

print("\n=== 3. PRODUITS ===")
h, d_p_cat = read_xlsx(os.path.join(base_dir, 'produits_catalogue.xlsx'))
print("produits_catalogue.xlsx columns:", h)
print("sample row 1:", d_p_cat[0])

with open(os.path.join(base_dir, 'produits_fournisseurs.csv'), 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    print("produits_fournisseurs.csv columns:", r.fieldnames)
    d_p_four = list(r)
    print("sample row 1:", d_p_four[0])

print("\n=== 4. VENTES ===")
h, d_v = read_xlsx(os.path.join(base_dir, 'ventes_synthese.xlsx'))
print("ventes_synthese.xlsx columns:", h)
print("sample row 1:", d_v[0])
