import os

tp2_process_dir = r"C:\Users\pc\Downloads\TOS_DI-20261018_1914-V8.9.0SNAPSHOT-win32.win32.x86_64\workspace\TP2_BI_VENTES\process"

# In Job_Dim_Client_Ventes, replace the schema of tDBOutput_1 with the exact client columns
client_file = os.path.join(tp2_process_dir, "Job_Dim_Client_Ventes_0.1.item")
with open(client_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace departement and niveau references
text = text.replace('value="departement"', 'value="ville"')
text = text.replace('value="niveau"', 'value="email"')
text = text.replace('name="departement"', 'name="ville"')
text = text.replace('name="niveau"', 'name="email"')

with open(client_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Job_Dim_Client_Ventes.")
