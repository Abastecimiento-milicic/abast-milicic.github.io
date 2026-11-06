import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

csv_path = "data/Almacen MB52/Combinados/MB52_CONSOLIDADO_COMBINADO.csv"
df = pd.read_csv(csv_path, sep=';', encoding='latin1', low_memory=False)

print("Total rows in MB52 Consolidado:", len(df))
planif_no = df[df['Planificado'] == 'NO']
print("Total Planificado = NO:", len(planif_no))
print("Planificado = NO with empty 'Tipo material':", len(planif_no[planif_no['Tipo material'].isna() | (planif_no['Tipo material'].astype(str).str.strip() == '')]))
print("Planificado = NO with filled 'Tipo material':", len(planif_no[~planif_no['Tipo material'].isna() & (planif_no['Tipo material'].astype(str).str.strip() != '')]))

planif_si = df[df['Planificado'] == 'SI']
print("Total Planificado = SI:", len(planif_si))
print("Planificado = SI with empty 'Tipo material':", len(planif_si[planif_si['Tipo material'].isna() | (planif_si['Tipo material'].astype(str).str.strip() == '')]))
print("Planificado = SI with filled 'Tipo material':", len(planif_si[~planif_si['Tipo material'].isna() & (planif_si['Tipo material'].astype(str).str.strip() != '')]))
