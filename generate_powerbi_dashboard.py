import json
import os
import subprocess
import pandas as pd

def clean_region(r):
    if not isinstance(r, str):
        return "Non specifie"
    if "Tanger" in r:
        return "Tanger-Tetouan-Al Hoceima"
    if "Rabat" in r:
        return "Rabat-Sale-Kenitra"
    if "Tafilalet" in r or "Dr" in r:
        return "Draa-Tafilalet"
    if "F" in r and "Mekn" in r:
        return "Fes-Meknes"
    if "Casablanca" in r:
        return "Grand Casablanca"
    if "Marrakech" in r:
        return "Marrakech-Safi"
    if "Oriental" in r:
        return "Oriental"
    if "Souss" in r:
        return "Souss-Massa"
    return r

def clean_mode(m):
    if not isinstance(m, str):
        return "Autre"
    if "Esp" in m:
        return "Especes"
    if "Ch" in m:
        return "Cheque"
    if "Carte" in m:
        return "Carte bancaire"
    if "mobile" in m:
        return "Paiement mobile"
    if "Vir" in m:
        return "Virement"
    return m

def clean_mag(m):
    if not isinstance(m, str):
        return "Magasin"
    if "F" in m and "Commerce" in m:
        return "Fes Commerce"
    return m

df_fait = pd.read_csv('donnees_powerbi/fait_ventes.csv')
df_client = pd.read_csv('donnees_powerbi/dim_client.csv')
df_produit = pd.read_csv('donnees_powerbi/dim_produit.csv')
df_magasin = pd.read_csv('donnees_powerbi/dim_magasin.csv')
df_temps = pd.read_csv('donnees_powerbi/dim_temps.csv')

df_magasin['region'] = df_magasin['region'].apply(clean_region)
df_magasin['nom_magasin'] = df_magasin['nom_magasin'].apply(clean_mag)
df_fait['mode_paiement'] = df_fait['mode_paiement'].apply(clean_mode)

ca_total = df_fait['montant_total'].sum()
qte_totale = int(df_fait['quantite_vendue'].sum())
nb_trans = len(df_fait)
panier_moyen = df_fait['montant_total'].mean()

# Merge for aggregations
m_mag = df_fait.merge(df_magasin, left_on='id_magasin_fk', right_on='id_magasin_sk')
ca_reg = m_mag.groupby('region')['montant_total'].sum().sort_values(ascending=False).reset_index()

m_prod = df_fait.merge(df_produit, left_on='id_produit_fk', right_on='id_produit_sk')
ca_cat = m_prod.groupby('categorie')['montant_total'].sum().sort_values(ascending=False).reset_index()

ca_pm = df_fait.groupby('mode_paiement')['montant_total'].sum().sort_values(ascending=False).reset_index()

m_temps = df_fait.merge(df_temps, left_on='id_temps_fk', right_on='id_temps')
ca_annee = m_temps.groupby('annee')['montant_total'].sum().reset_index()

# Top 5 transactions
top5 = df_fait.merge(df_client, left_on='id_client_fk', right_on='id_client_sk') \
              .merge(df_produit, left_on='id_produit_fk', right_on='id_produit_sk') \
              .merge(df_magasin, left_on='id_magasin_fk', right_on='id_magasin_sk') \
              .sort_values(by='montant_total', ascending=False).head(5)

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Power BI - Tableau de Bord Decisionnel Ventes</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: #F1F5F9; color: #0F172A; padding: 24px; }}
        
        .pbi-navbar {{
            background: #111827;
            color: white;
            padding: 14px 24px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 6px solid #F59E0B;
        }}
        .pbi-brand {{ display: flex; align-items: center; gap: 12px; }}
        .pbi-tag {{ background: #F59E0B; color: #000; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px; }}
        .pbi-title-text {{ font-size: 19px; font-weight: 700; }}
        .pbi-subtitle {{ font-size: 12px; color: #94A3B8; margin-top: 2px; }}
        .pbi-author-box {{ text-align: right; font-size: 12px; color: #CBD5E1; line-height: 1.5; }}
        .pbi-author-box strong {{ color: #FFFFFF; }}

        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }}
        .kpi-card {{
            background: #FFFFFF;
            padding: 18px 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            position: relative;
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 4px;
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
        }}
        .kpi-blue::before {{ background: #2563EB; }}
        .kpi-emerald::before {{ background: #059669; }}
        .kpi-amber::before {{ background: #D97706; }}
        .kpi-indigo::before {{ background: #4F46E5; }}

        .kpi-label {{ font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.6px; }}
        .kpi-val {{ font-size: 26px; font-weight: 800; color: #0F172A; margin: 8px 0 4px 0; }}
        .kpi-sub {{ font-size: 11px; color: #059669; font-weight: 600; display: flex; align-items: center; gap: 4px; }}

        .row-grid {{
            display: grid;
            grid-template-columns: 2fr 1.1fr;
            gap: 16px;
            margin-bottom: 16px;
        }}
        .panel {{
            background: #FFFFFF;
            padding: 18px 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            margin-bottom: 12px;
            border-bottom: 1px solid #F1F5F9;
        }}
        .panel-title {{ font-size: 14px; font-weight: 700; color: #1E293B; }}
        .panel-tag {{ font-size: 11px; font-weight: 600; color: #64748B; background: #F1F5F9; padding: 2px 8px; border-radius: 4px; }}

        .chart-box {{ position: relative; height: 250px; width: 100%; }}

        table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
        th {{ background: #F8FAFC; color: #475569; font-weight: 700; text-align: left; padding: 9px 10px; border-bottom: 2px solid #E2E8F0; font-size: 11.5px; text-transform: uppercase; }}
        td {{ padding: 9px 10px; border-bottom: 1px solid #F1F5F9; color: #334155; }}
        tr:last-child td {{ border-bottom: none; }}
        .badge-mode {{ padding: 3px 7px; border-radius: 4px; font-size: 11px; font-weight: 600; background: #EFF6FF; color: #1D4ED8; }}
    </style>
</head>
<body>

    <div class="pbi-navbar">
        <div class="pbi-brand">
            <span class="pbi-tag">POWER BI</span>
            <div>
                <div class="pbi-title-text">Tableau de Bord Decisionnel - Data Warehouse Ventes</div>
                <div class="pbi-subtitle">Schema en Etoile | Alimentation ETL Talaxie | Source MySQL : dwh_ventes</div>
            </div>
        </div>
        <div class="pbi-author-box">
            <div>Etudiant : <strong>LAHSAINI Yassine</strong> (Master TEE S3)</div>
            <div>Enseignante : <strong>Pr. Oumaima STITINI</strong></div>
            <div>Universite Cadi Ayyad - ENS Marrakech</div>
        </div>
    </div>

    <div class="kpi-container">
        <div class="kpi-card kpi-blue">
            <div class="kpi-label">Chiffre d'Affaires Total</div>
            <div class="kpi-val">{ca_total:,.2f} DH</div>
            <div class="kpi-sub">50 transactions consolidees</div>
        </div>
        <div class="kpi-card kpi-emerald">
            <div class="kpi-label">Volume Total Vendu</div>
            <div class="kpi-val">{qte_totale:,} unites</div>
            <div class="kpi-sub">100% integrite stock</div>
        </div>
        <div class="kpi-card kpi-amber">
            <div class="kpi-label">Panier Moyen</div>
            <div class="kpi-val">{panier_moyen:,.2f} DH</div>
            <div class="kpi-sub">Moyenne par vente</div>
        </div>
        <div class="kpi-card kpi-indigo">
            <div class="kpi-label">Transactions Realisees</div>
            <div class="kpi-val">{nb_trans}</div>
            <div class="kpi-sub">8 regions de distribution</div>
        </div>
    </div>

    <div class="row-grid">
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Chiffre d'Affaires par Region Administrative (DH)</span>
                <span class="panel-tag">dim_magasin</span>
            </div>
            <div class="chart-box">
                <canvas id="chartRegion"></canvas>
            </div>
        </div>
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Chiffre d'Affaires par Mode de Reglement</span>
                <span class="panel-tag">fait_ventes</span>
            </div>
            <div class="chart-box">
                <canvas id="chartPaiement"></canvas>
            </div>
        </div>
    </div>

    <div class="row-grid">
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Evolution Annuelle du Chiffre d'Affaires (2023 - 2025)</span>
                <span class="panel-tag">dim_temps</span>
            </div>
            <div class="chart-box">
                <canvas id="chartAnnee"></canvas>
            </div>
        </div>
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Top 5 des Transactions les Plus Importantes</span>
                <span class="panel-tag">Audit Faits</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Client</th>
                        <th>Magasin</th>
                        <th>Montant</th>
                        <th>Reglement</th>
                    </tr>
                </thead>
                <tbody>
"""

for _, row in top5.iterrows():
    nom_cli = row['nom_complet'] if pd.notna(row['nom_complet']) else 'Client Inconnu'
    nom_mag = clean_mag(row['nom_magasin'])
    mp = clean_mode(row['mode_paiement'])
    html_content += f"""
                    <tr>
                        <td><strong>{row['code_vente']}</strong></td>
                        <td>{nom_cli}</td>
                        <td>{nom_mag}</td>
                        <td><strong>{row['montant_total']:,.2f} DH</strong></td>
                        <td><span class="badge-mode">{mp}</span></td>
                    </tr>
"""

html_content += f"""
                </tbody>
            </table>
        </div>
    </div>

    <script>
        new Chart(document.getElementById('chartRegion'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(ca_reg['region']))},
                datasets: [{{
                    data: {json.dumps(list(ca_reg['montant_total']))},
                    backgroundColor: '#2563EB',
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#F1F5F9' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        new Chart(document.getElementById('chartPaiement'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(ca_pm['mode_paiement']))},
                datasets: [{{
                    data: {json.dumps(list(ca_pm['montant_total']))},
                    backgroundColor: ['#059669', '#2563EB', '#D97706', '#4F46E5', '#DC2626']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }}
                }}
            }}
        }});

        new Chart(document.getElementById('chartAnnee'), {{
            type: 'line',
            data: {{
                labels: {json.dumps([str(x) for x in ca_annee['annee']])},
                datasets: [{{
                    data: {json.dumps(list(ca_annee['montant_total']))},
                    borderColor: '#2563EB',
                    backgroundColor: 'rgba(37, 99, 235, 0.08)',
                    fill: true,
                    tension: 0.25,
                    borderWidth: 3,
                    pointBackgroundColor: '#2563EB',
                    pointRadius: 5
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#F1F5F9' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

html_path = r"C:\Users\pc\OneDrive\Bureau\ETL\Dashboard_Ventes_BI.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

png_path = r"C:\Users\pc\OneDrive\Bureau\ETL\images\dashboard_power_bi.png"
edge_cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless=new",
    "--disable-gpu",
    f"--screenshot={png_path}",
    "--window-size=1600,1050",
    f"file:///{html_path.replace(os.sep, '/')}"
]

subprocess.run(edge_cmd, check=True)
print(f"Capture haute resolution mise a jour : {png_path} ({os.path.getsize(png_path)} octets)")
