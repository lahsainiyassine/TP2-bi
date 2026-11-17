import os, csv, zipfile, datetime
import xml.etree.ElementTree as ET

base_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\Etude de cas DW Fichiers Sources\Etude de cas DW"

def excel_date(val):
    try:
        n = float(val)
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
        
        header_keys = sorted(rows[0].keys())
        headers = [rows[0][k] for k in header_keys]
        data = []
        for r in rows[1:]:
            data.append({rows[0][k]: r.get(k) for k in header_keys})
        return headers, data

# Inspect ventes calculations
_, ventes = read_xlsx(os.path.join(base_dir, 'ventes_synthese.xlsx'))
print("=== VENTES ANALYSIS ===")
calc_diffs = []
for v in ventes:
    vid = v['id_vente']
    q = float(v['quantite_vendue'])
    p = float(v['prix_unitaire'])
    mt = float(v['montant_total'])
    expected = round(q * p, 2)
    diff = round(mt - expected, 2)
    if abs(diff) > 0.01:
        calc_diffs.append((vid, q, p, mt, expected, diff))

print(f"Total ventes: {len(ventes)}")
print(f"Ventes where montant_total != quantite * prix_unitaire: {len(calc_diffs)}")
if calc_diffs:
    print("Sample differences:", calc_diffs[:5])

# Check nulls in each file
print("\n=== NULL CHECKS ===")
for f in os.listdir(base_dir):
    full_path = os.path.join(base_dir, f)
    if f.endswith('.xlsx'):
        h, d = read_xlsx(full_path)
        null_counts = {col: sum(1 for row in d if row.get(col) is None or str(row.get(col)).strip() == '') for col in h}
        print(f"XLSX {f}: {null_counts}")
    elif f.endswith('.csv'):
        with open(full_path, 'r', encoding='utf-8') as fp:
            r = csv.DictReader(fp)
            d = list(r)
            null_counts = {col: sum(1 for row in d if row.get(col) is None or str(row.get(col)).strip() == '') for col in r.fieldnames}
            print(f"CSV {f}: {null_counts}")
    elif f.endswith('.xml'):
        tree = ET.parse(full_path)
        d = [{el.tag: el.text for el in c} for c in tree.getroot()]
        keys = list(d[0].keys()) if d else []
        null_counts = {k: sum(1 for row in d if row.get(k) is None or str(row.get(k)).strip() == '') for k in keys}
        print(f"XML {f}: {null_counts}")

