import subprocess
import os

out_dir = r"C:\Users\pc\OneDrive\Bureau\ETL\donnees_powerbi"
os.makedirs(out_dir, exist_ok=True)

tables = ['dim_client', 'dim_produit', 'dim_magasin', 'dim_temps', 'fait_ventes']
for t in tables:
    cmd = f'C:\\xampp\\mysql\\bin\\mysql.exe -u root -e "SELECT * FROM dwh_ventes.{t};"'
    res = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
    csv_path = os.path.join(out_dir, f"{t}.csv")
    lines = res.strip().split('\n')
    with open(csv_path, 'w', encoding='utf-8') as f:
        for line in lines:
            parts = line.split('\t')
            f.write(','.join(['"' + p.strip() + '"' for p in parts]) + '\n')
    print(f"Exported {t} ({len(lines)-1} lignes) vers {csv_path}")

print("Exportation terminee avec succes !")
