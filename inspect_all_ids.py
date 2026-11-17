import os, csv, zipfile
import xml.etree.ElementTree as ET

base_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\Etude de cas DW Fichiers Sources\Etude de cas DW"

def get_xlsx_ids(filename, col_idx=0):
    with zipfile.ZipFile(os.path.join(base_dir, filename), 'r') as z:
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
        target_k = h_keys[col_idx]
        return [r.get(target_k) for r in rows[1:]]

# clients
c_base_ids = get_xlsx_ids('clients_base_50.xlsx', 0)
with open(os.path.join(base_dir, 'clients_online_50.csv'), 'r', encoding='utf-8') as f:
    c_online_ids = [r[0] for r in csv.reader(f)][1:]
tree = ET.parse(os.path.join(base_dir, 'clients_fidelite_50.xml'))
c_fid_ids = [el.find('id').text for el in tree.getroot()]

print("c_base_ids:", len(c_base_ids), c_base_ids[:5], "...", c_base_ids[-5:])
print("c_online_ids:", len(c_online_ids), c_online_ids[:5], "...", c_online_ids[-5:])
print("c_fid_ids:", len(c_fid_ids), c_fid_ids[:5], "...", c_fid_ids[-5:])

# products
p_cat_ids = get_xlsx_ids('produits_catalogue.xlsx', 0)
with open(os.path.join(base_dir, 'produits_fournisseurs.csv'), 'r', encoding='utf-8') as f:
    p_four_ids = [r[0] for r in csv.reader(f)][1:]
print("p_cat_ids:", len(p_cat_ids), p_cat_ids[:5], "...", p_cat_ids[-5:])
print("p_four_ids:", len(p_four_ids), p_four_ids[:5], "...", p_four_ids[-5:])

# magasins
with open(os.path.join(base_dir, 'magasins_localisation (2).csv'), 'r', encoding='utf-8') as f:
    m_loc_ids = [r[0] for r in csv.reader(f)][1:]
m_ven_ids = get_xlsx_ids('magasins_ventes (1).xlsx', 0)
print("m_loc_ids:", len(m_loc_ids), m_loc_ids[:5], "...", m_loc_ids[-5:])
print("m_ven_ids:", len(m_ven_ids), m_ven_ids[:5], "...", m_ven_ids[-5:])

# ventes
v_ids = get_xlsx_ids('ventes_synthese.xlsx', 0)
v_c_ids = get_xlsx_ids('ventes_synthese.xlsx', 1)
v_p_ids = get_xlsx_ids('ventes_synthese.xlsx', 2)
v_m_ids = get_xlsx_ids('ventes_synthese.xlsx', 3)
print("v_c_ids:", len(v_c_ids), sorted(set(v_c_ids)))
print("v_p_ids:", len(v_p_ids), sorted(set(v_p_ids)))
print("v_m_ids:", len(v_m_ids), sorted(set(v_m_ids)))
