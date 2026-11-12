import os

js_dir = r"c:\Users\david.benitez\Documents\GitHub\abast-milicic.github.io\js"

def update_file(filename, replacements):
    fpath = os.path.join(js_dir, filename)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    for old, new in replacements:
        if old not in content:
            print(f"[WARN] In {filename}: target not found: {old}")
        else:
            content = content.replace(old, new)
            print(f"[OK] In {filename}: replaced {old} -> {new}")
            
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

# 1. analisis-mm.js
update_file("analisis-mm.js", [
    ('const csvUrl = "data/ANALISIS-MM.csv";', 'const csvUrl = "data/data ANALISIS MM/ANALISIS-MM.csv";'),
    ('1: "data/STO NULO.csv",', '1: "data/data ANALISIS MM/STO NULO.csv",'),
    ('2: "data/MENOR A PP.csv",', '2: "data/data ANALISIS MM/MENOR A PP.csv",'),
    ('3: "data/MAYOR AL PP.csv",', '3: "data/data ANALISIS MM/MAYOR AL PP.csv",'),
    ('4: "data/MAYOR STOCK MAX.csv"', '4: "data/data ANALISIS MM/MAYOR STOCK MAX.csv"'),
    ('downloadExternalFilteredCSV("data/STO NULO.csv");', 'downloadExternalFilteredCSV("data/data ANALISIS MM/STO NULO.csv");'),
    ('downloadExternalFilteredCSV("data/MENOR A PP.csv");', 'downloadExternalFilteredCSV("data/data ANALISIS MM/MENOR A PP.csv");'),
    ('downloadByEstadoValue("Mayor a Stock Maximo", "data/MAYOR STOCK MAX.csv");', 'downloadByEstadoValue("Mayor a Stock Maximo", "data/data ANALISIS MM/MAYOR STOCK MAX.csv");'),
    ('downloadStaticFile("data/Stock Base Obra 0374.csv")', 'downloadStaticFile("data/data ANALISIS MM/Stock Base Obra 0374.csv")'),
    ('downloadStaticFile("data/Stock Base Obra 0378.csv")', 'downloadStaticFile("data/data ANALISIS MM/Stock Base Obra 0378.csv")')
])

# 2. control-emrf.js
update_file("control-emrf.js", [
    ('const JSON_URL = "data/partidas_emrf.json";', 'const JSON_URL = "data/data PARTIDAS ABIERTAS/partidas_emrf.json";')
])

# 3. cumplimiento-arriba.js
update_file("cumplimiento-arriba.js", [
    ('const CSV_ARRIBA_URL = "data/Base_Final_365_372.csv";', 'const CSV_ARRIBA_URL = "data/data CUMPLIMIENTO/Base_Final_365_372.csv";'),
    ('const XLSX_ARRIBA_URL = "data/Base_Final_365_372.xlsx";', 'const XLSX_ARRIBA_URL = "data/data CUMPLIMIENTO/Base_Final_365_372.xlsx";')
])

# 4. cumplimiento.js
update_file("cumplimiento.js", [
    ('abastecimiento: "data/CUMPLIMIENTO_OPTIMIZADO.csv",', 'abastecimiento: "data/data CUMPLIMIENTO/CUMPLIMIENTO_OPTIMIZADO.csv",')
])

# 5. demoras.js
update_file("demoras.js", [
    ('const csvUrl = "data/CUMPLIMIENTO_OPTIMIZADO.csv";', 'const csvUrl = "data/data CUMPLIMIENTO/CUMPLIMIENTO_OPTIMIZADO.csv";')
])

# 6. evolucion.js
update_file("evolucion.js", [
    ('const EVOL_URL = "data/EVOLUCION.csv";', 'const EVOL_URL = "data/data ANALISIS MM/EVOLUCION.csv";')
])

# 7. resumen.js
update_file("resumen.js", [
    ('const CSV_MM_URL = "data/ANALISIS-MM.csv";', 'const CSV_MM_URL = "data/data ANALISIS MM/ANALISIS-MM.csv";'),
    ('const CSV_STONULO_URL = "data/STO NULO.csv";', 'const CSV_STONULO_URL = "data/data ANALISIS MM/STO NULO.csv";'),
    ('const CSV_CUMPL_URL = "data/CUMPLIMIENTO_OPTIMIZADO.csv";', 'const CSV_CUMPL_URL = "data/data CUMPLIMIENTO/CUMPLIMIENTO_OPTIMIZADO.csv";'),
    ('const CSV_ARRIBA_URL = "data/Base_Final_365_372.csv";', 'const CSV_ARRIBA_URL = "data/data CUMPLIMIENTO/Base_Final_365_372.csv";'),
    ('const CSV_SERV_URL = "data/SERVICIOS OBRA.csv";', 'const CSV_SERV_URL = "data/data SERVICIOS/SERVICIOS OBRA.csv";'),
    ('const CSV_EVOL_URL = "data/EVOLUCION.csv";', 'const CSV_EVOL_URL = "data/data ANALISIS MM/EVOLUCION.csv";'),
    ('const JSON_EMRF_URL = "data/partidas_emrf.json";', 'const JSON_EMRF_URL = "data/data PARTIDAS ABIERTAS/partidas_emrf.json";')
])

# 8. servicios.js
update_file("servicios.js", [
    ('abastecimiento: "data/SERVICIOS OBRA.csv"', 'abastecimiento: "data/data SERVICIOS/SERVICIOS OBRA.csv"')
])

# 9. tiempos-entrega.js
update_file("tiempos-entrega.js", [
    ('const csvUrl = "data/CUMPLIMIENTO_OPTIMIZADO.csv";', 'const csvUrl = "data/data CUMPLIMIENTO/CUMPLIMIENTO_OPTIMIZADO.csv";')
])

print("All files updated successfully!")
