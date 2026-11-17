import os, shutil

src_process = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\MINI_PROJET\process"
dst_process = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\TP2_BI_VENTES\process"

jobs = [
    "Job_Dim_Client_Ventes",
    "Job_Dim_Produit_Ventes",
    "Job_Dim_Magasin_Ventes",
    "Job_Dim_Temps_Ventes",
    "Job_Fait_Ventes"
]

for j in jobs:
    for ext in [".item", ".properties"]:
        src_file = os.path.join(src_process, f"{j}_0.1{ext}")
        dst_file = os.path.join(dst_process, f"{j}_0.1{ext}")
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
            print(f"Copied {j}_0.1{ext} to TP2_BI_VENTES")

# Also copy DB connection
src_conn = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\MINI_PROJET\metadata\connections"
dst_conn = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\TP2_BI_VENTES\metadata\connections"

for f in os.listdir(src_conn):
    if f.startswith("conn_dw"):
        s = os.path.join(src_conn, f)
        d = os.path.join(dst_conn, f)
        with open(s, 'r', encoding='utf-8') as fp:
            content = fp.read()
        content = content.replace("dw_universite", "dwh_ventes")
        with open(d, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Copied & adapted connection {f}")

print("Sync to TP2_BI_VENTES completed!")
