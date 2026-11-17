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

# Inspect clients comparison
_, c_base = read_xlsx(os.path.join(base_dir, 'clients_base_50.xlsx'))
with open(os.path.join(base_dir, 'clients_online_50.csv'), 'r', encoding='utf-8') as f:
    c_online = list(csv.DictReader(f))

tree = ET.parse(os.path.join(base_dir, 'clients_fidelite_50.xml'))
c_fidelite = {el.find('id').text: {'points': el.find('points').text, 'carte': el.find('carte').text} for el in tree.getroot()}

print("--- Comparison of first 5 clients across Base, Online, Fidelite ---")
for i in range(5):
    cb = c_base[i]
    cid = cb['client_id']
    co = next((x for x in c_online if x['client_code'] == cid), None)
    cf = c_fidelite.get(cid)
    print(f"ID: {cid}")
    print(f"  Base   : Nom={cb.get('nom')}, Prenom={cb.get('prenom')}, Ville={cb.get('ville')}, Email={cb.get('email')}, Date={excel_date(cb.get('date_inscription'))}, Seg={cb.get('segment_marketing')}")
    if co:
        print(f"  Online : FullName={co.get('full_name')}, Ville={co.get('city')}, Email={co.get('email')}, FirstDate={co.get('first_purchase_date')}")
    if cf:
        print(f"  Fidélité: Points={cf.get('points')}, Carte={cf.get('carte')}")

# Check differences between base and online
print("\n--- Discrepancies between Base and Online for same ID ---")
diff_count = 0
for cb in c_base:
    cid = cb['client_id']
    co = next((x for x in c_online if x['client_code'] == cid), None)
    if co:
        full_base = f"{cb.get('prenom')} {cb.get('nom')}".strip()
        full_base_inv = f"{cb.get('nom')} {cb.get('prenom')}".strip()
        diffs = []
        if cb.get('email') != co.get('email'):
            diffs.append(f"email: base='{cb.get('email')}' vs online='{co.get('email')}'")
        if cb.get('ville') != co.get('city'):
            diffs.append(f"ville: base='{cb.get('ville')}' vs online='{co.get('city')}'")
        if co.get('full_name') not in [full_base, full_base_inv]:
            diffs.append(f"name: base='{full_base}' vs online='{co.get('full_name')}'")
        if diffs:
            diff_count += 1
            if diff_count <= 5:
                print(f"Client {cid}:", ", ".join(diffs))
print(f"Total clients with differences: {diff_count} / 50")

# Inspect Dates across all sources for dim_temps
print("\n--- Dates inspection across sources ---")
# 1. clients_base date_inscription
dates_cb = [excel_date(cb.get('date_inscription')) for cb in c_base if cb.get('date_inscription')]
# 2. clients_online first_purchase_date
dates_co = [co.get('first_purchase_date') for co in c_online if co.get('first_purchase_date')]
# 3. magasins_localisation date_ouverture
with open(os.path.join(base_dir, 'magasins_localisation (2).csv'), 'r', encoding='utf-8') as f:
    m_loc = list(csv.DictReader(f))
dates_ml = [m.get('date_ouverture') for m in m_loc if m.get('date_ouverture')]
# 4. produits_catalogue date_insertion
_, p_cat = read_xlsx(os.path.join(base_dir, 'produits_catalogue.xlsx'))
dates_pc = [excel_date(p.get('date_insertion')) for p in p_cat if p.get('date_insertion')]
# 5. ventes_synthese date_vente
_, v_syn = read_xlsx(os.path.join(base_dir, 'ventes_synthese.xlsx'))
dates_vs = [excel_date(v.get('date_vente')) for v in v_syn if v.get('date_vente')]

all_dates = set(dates_cb + dates_co + dates_ml + dates_pc + dates_vs)
print(f"Count of dates in clients_base: {len(dates_cb)} (min: {min(dates_cb)}, max: {max(dates_cb)})")
print(f"Count of dates in clients_online: {len(dates_co)} (min: {min(dates_co)}, max: {max(dates_co)})")
print(f"Count of dates in magasins_localisation: {len(dates_ml)} (min: {min(dates_ml)}, max: {max(dates_ml)})")
print(f"Count of dates in produits_catalogue: {len(dates_pc)} (min: {min(dates_pc)}, max: {max(dates_pc)})")
print(f"Count of dates in ventes_synthese: {len(dates_vs)} (min: {min(dates_vs)}, max: {max(dates_vs)})")
print(f"Total unique dates across all sources: {len(all_dates)}")

