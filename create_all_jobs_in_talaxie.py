import os
import shutil
import uuid
import xml.etree.ElementTree as ET

process_dir = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\MINI_PROJET\process"
sources_dir = r"C:/Users/pc/OneDrive/Bureau/ETL/Etude de cas DW Fichiers Sources/Etude de cas DW"

def make_id():
    return "_" + uuid.uuid4().hex[:22]

def create_properties_file(job_name):
    prop_path = os.path.join(process_dir, f"{job_name}_0.1.properties")
    prop_xmi_id = make_id()
    prop_id = make_id()
    item_xmi_id = make_id()
    state_xmi_id = make_id()
    add_ids = [make_id() for _ in range(6)]
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:TalendProperties="http://www.talend.org/properties">
  <TalendProperties:Property xmi:id="{prop_xmi_id}" id="{prop_id}" label="{job_name}" version="0.1" statusCode="" item="{item_xmi_id}" displayName="{job_name}">
    <author href="../talend.project#_9EEDoM9UEfG71M3VwE5zwA"/>
    <additionalProperties xmi:id="{add_ids[0]}" key="created_product_fullname" value="Talaxie Open Studio for Data Integration"/>
    <additionalProperties xmi:id="{add_ids[1]}" key="created_product_version" value="8.9.0.20261020-1837-SNAPSHOT"/>
    <additionalProperties xmi:id="{add_ids[2]}" key="created_date" value="2026-11-17T17:00:00.000+0000"/>
    <additionalProperties xmi:id="{add_ids[3]}" key="modified_product_fullname" value="Talaxie Open Studio for Data Integration"/>
    <additionalProperties xmi:id="{add_ids[4]}" key="modified_product_version" value="8.9.0.20261018-1926-SNAPSHOT"/>
    <additionalProperties xmi:id="{add_ids[5]}" key="modified_date" value="2026-11-17T17:45:00.000+0100"/>
  </TalendProperties:Property>
  <TalendProperties:ItemState xmi:id="{state_xmi_id}" path=""/>
  <TalendProperties:ProcessItem xmi:id="{item_xmi_id}" property="{prop_xmi_id}" state="{state_xmi_id}">
    <process href="{job_name}_0.1.item#/"/>
  </TalendProperties:ProcessItem>
</xmi:XMI>"""
    with open(prop_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Created {job_name}_0.1.properties")

# 1. JOB_DIM_CLIENT_VENTES
# Based on Job_Dim_Filiere_0.1.item template
template_filiere = os.path.join(process_dir, "Job_Dim_Filiere_0.1.item")
with open(template_filiere, 'r', encoding='utf-8') as f:
    client_item = f.read()

# Update parameters for clients
client_item = client_item.replace("C:/Users/pc/Downloads/Filieres.xlsx", f"{sources_dir}/clients_base_50.xlsx")
client_item = client_item.replace('"dw_universite"', '"dwh_ventes"')
client_item = client_item.replace('"dim_filiere"', '"dim_client"')
client_item = client_item.replace('dim_filiere', 'dim_client')
with open(os.path.join(process_dir, "Job_Dim_Client_Ventes_0.1.item"), 'w', encoding='utf-8') as f:
    f.write(client_item)
create_properties_file("Job_Dim_Client_Ventes")

# 2. JOB_DIM_PRODUIT_VENTES
produit_item = client_item.replace(f"{sources_dir}/clients_base_50.xlsx", f"{sources_dir}/produits_catalogue.xlsx")
produit_item = produit_item.replace('"dim_client"', '"dim_produit"')
produit_item = produit_item.replace('dim_client', 'dim_produit')
with open(os.path.join(process_dir, "Job_Dim_Produit_Ventes_0.1.item"), 'w', encoding='utf-8') as f:
    f.write(produit_item)
create_properties_file("Job_Dim_Produit_Ventes")

# 3. JOB_DIM_MAGASIN_VENTES
magasin_item = client_item.replace(f"{sources_dir}/clients_base_50.xlsx", f"{sources_dir}/magasins_ventes (1).xlsx")
magasin_item = magasin_item.replace('"dim_client"', '"dim_magasin"')
magasin_item = magasin_item.replace('dim_client', 'dim_magasin')
with open(os.path.join(process_dir, "Job_Dim_Magasin_Ventes_0.1.item"), 'w', encoding='utf-8') as f:
    f.write(magasin_item)
create_properties_file("Job_Dim_Magasin_Ventes")

# 4. JOB_DIM_TEMPS_VENTES
# Based on Job_Dim_Temps_0.1.item
template_temps = os.path.join(process_dir, "Job_Dim_Temps_0.1.item")
with open(template_temps, 'r', encoding='utf-8') as f:
    temps_item = f.read()

temps_item = temps_item.replace('"dw_universite"', '"dwh_ventes"')
temps_item = temps_item.replace("C:/Users/pc/Downloads/Inscriptions.xlsx", f"{sources_dir}/ventes_synthese.xlsx")
with open(os.path.join(process_dir, "Job_Dim_Temps_Ventes_0.1.item"), 'w', encoding='utf-8') as f:
    f.write(temps_item)
create_properties_file("Job_Dim_Temps_Ventes")

# 5. JOB_FAIT_VENTES
template_fait = os.path.join(process_dir, "Job_Fait_Inscription_0.1.item")
with open(template_fait, 'r', encoding='utf-8') as f:
    fait_item = f.read()

fait_item = fait_item.replace('"dw_universite"', '"dwh_ventes"')
fait_item = fait_item.replace("C:/Users/pc/Downloads/Inscriptions.xlsx", f"{sources_dir}/ventes_synthese.xlsx")
fait_item = fait_item.replace('"fait_inscription"', '"fait_ventes"')
fait_item = fait_item.replace('fait_inscription', 'fait_ventes')
with open(os.path.join(process_dir, "Job_Fait_Ventes_0.1.item"), 'w', encoding='utf-8') as f:
    f.write(fait_item)
create_properties_file("Job_Fait_Ventes")

print("All 5 jobs successfully created in MINI_PROJET process directory!")
