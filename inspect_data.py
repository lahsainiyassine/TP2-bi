import os
import csv
import xml.etree.ElementTree as ET
import zipfile
import json

base_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\Etude de cas DW Fichiers Sources\Etude de cas DW"

def read_xlsx(path):
    with zipfile.ZipFile(path, 'r') as z:
        # read shared strings if exists
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            # namespace
            ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            for si in tree.findall('ns:si', ns):
                t = si.find('ns:t', ns)
                if t is not None and t.text:
                    shared_strings.append(t.text)
                else:
                    # check nested text
                    texts = [elem.text for elem in si.iter() if elem.text]
                    shared_strings.append("".join(texts))
        
        # read workbook to get sheet names
        wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
        ns_wb = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
                 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
        sheets = []
        for s in wb_tree.findall('ns:sheets/ns:sheet', ns_wb):
            sheets.append(s.attrib['name'])
        
        # let's read sheet1.xml
        sheet_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        ns_s = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        
        rows_data = []
        for row in sheet_tree.findall('.//ns:row', ns_s):
            r_idx = row.attrib.get('r')
            row_cells = {}
            for c in row.findall('ns:c', ns_s):
                col_ref = c.attrib.get('r') # e.g. A1, B1
                t = c.attrib.get('t') # s for shared string
                v = c.find('ns:v', ns_s)
                val = v.text if v is not None else None
                if val is not None:
                    if t == 's':
                        val = shared_strings[int(val)]
                row_cells[col_ref] = val
            rows_data.append(row_cells)
        return sheets, rows_data

def inspect_all():
    files = os.listdir(base_dir)
    print("Files found:", files)
    
    for f in files:
        full_path = os.path.join(base_dir, f)
        print("\n" + "="*80)
        print(f"FILE: {f} (Size: {os.path.getsize(full_path)} bytes)")
        print("="*80)
        
        if f.endswith('.csv'):
            # try detecting delimiter
            with open(full_path, 'r', encoding='utf-8', errors='replace') as fp:
                lines = [fp.readline() for _ in range(5)]
                delim = ';' if ';' in lines[0] else ','
            with open(full_path, 'r', encoding='utf-8', errors='replace') as fp:
                reader = csv.reader(fp, delimiter=delim)
                header = next(reader, None)
                print(f"Format: CSV, Delimiter: '{delim}'")
                print("Header:", header)
                count = 0
                sample = []
                for row in reader:
                    count += 1
                    if count <= 5:
                        sample.append(row)
                print(f"Total data rows: {count}")
                print("Sample rows:")
                for r in sample:
                    print("  ", r)
                    
        elif f.endswith('.xml'):
            tree = ET.parse(full_path)
            root = tree.getroot()
            print(f"Format: XML, Root tag: <{root.tag}>")
            children = list(root)
            print(f"Total child elements: {len(children)}")
            if len(children) > 0:
                print("Sample element tags and attributes/text:")
                for child in children[:3]:
                    c_dict = {elem.tag: elem.text for elem in child}
                    print(f"  <{child.tag}> attributes={child.attrib}: {c_dict}")
                    
        elif f.endswith('.xlsx'):
            sheets, rows = read_xlsx(full_path)
            print(f"Format: XLSX, Sheets: {sheets}")
            print(f"Total rows in sheet1: {len(rows)}")
            if rows:
                print("Header row keys:", list(rows[0].keys()))
                print("Header row values:", list(rows[0].values()))
                print("Sample data rows (next 3):")
                for r in rows[1:4]:
                    print("  ", list(r.values()))

inspect_all()
