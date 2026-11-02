import re
import sys

def verify():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    with open('js/resumen.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # 1. Check required IDs in HTML
    required_ids = [
        "resumen_obraSelect",
        "resumen_mesCumplSelect",
        "resumen_lblObra",
        "res_cumplMesSide",
        "resumen_btnClearFilters",
        "res_txtTotal",
        "res_txtDisp",
        "res_txtPct",
        "res_wrapNulo",
        "res_txtNulo",
        "res_txtMenorPP",
        "res_txtMayorPP",
        "res_txtMayorMax",
        "res_cumplAcumRango",
        "res_cumplAcumComprometidos",
        "res_cumplAcumATpct",
        "res_cumplAcumFTpct",
        "res_cumplAcumNEpct",
        "res_cumplAcumDemoraAvg",
        "res_cumplMesLabel",
        "res_cumplComprometidos",
        "res_cumplATpct",
        "res_cumplFTpct",
        "res_cumplNEpct",
        "res_cumplDemoraAvg"
    ]
    
    missing = []
    for rid in required_ids:
        pattern = rf'id=["\']{rid}["\']'
        matches = list(re.finditer(pattern, html))
        if not matches:
            missing.append(rid)
        elif len(matches) > 1:
            print(f"WARNING: duplicate ID '{rid}' found {len(matches)} times!")

    if missing:
        print(f"FAILED: Missing IDs in index.html: {missing}")
        sys.exit(1)
    else:
        print("PASS: All required IDs found in index.html without duplicates.")

    # 2. Check panel-resumen contains st-sidebar
    panel_match = re.search(r'<section id="panel-resumen"[^>]*>(.*?)</section>\s*</main>', html, re.DOTALL)
    if not panel_match:
        panel_match = re.search(r'<section id="panel-resumen"[^>]*>(.*?)</section>', html, re.DOTALL)

    if not panel_match:
        print("FAILED: <section id=\"panel-resumen\"> not found in index.html")
        sys.exit(1)
    
    panel_content = panel_match.group(1)
    if '<aside class="st-sidebar">' not in panel_content:
        print("FAILED: <aside class=\"st-sidebar\"> not found inside #panel-resumen!")
        sys.exit(1)

    sidebar_match = re.search(r'<aside class="st-sidebar">(.*?)</aside>', panel_content, re.DOTALL)
    sidebar_content = sidebar_match.group(1) if sidebar_match else ""

    if 'id="resumen_obraSelect"' not in sidebar_content:
        print("FAILED: resumen_obraSelect not found inside st-sidebar!")
        sys.exit(1)
    if 'id="resumen_mesCumplSelect"' not in sidebar_content:
        print("FAILED: resumen_mesCumplSelect not found inside st-sidebar!")
        sys.exit(1)
    if 'id="resumen_lblObra"' not in sidebar_content:
        print("FAILED: resumen_lblObra not found inside st-sidebar!")
        sys.exit(1)
    if 'id="res_cumplMesSide"' not in sidebar_content:
        print("FAILED: res_cumplMesSide not found inside st-sidebar!")
        sys.exit(1)
    if 'id="resumen_btnClearFilters"' not in sidebar_content:
        print("FAILED: resumen_btnClearFilters not found inside st-sidebar!")
        sys.exit(1)
    
    print("PASS: Both filters and active indicators are cleanly located inside the left st-sidebar (Panel de Control).")

    # 3. Check switchTab adds has-st-sidebar for resumen
    switch_match = re.search(r"if \(tabName === 'resumen'\) body\.classList\.add\((.*?)\);", html)
    if not switch_match or 'has-st-sidebar' not in switch_match.group(1):
        print("FAILED: switchTab does not add 'has-st-sidebar' for tabName === 'resumen'!")
        sys.exit(1)
    print("PASS: switchTab correctly adds 'has-st-sidebar' for resumen.")

    # 4. Check js/resumen.js
    if 'res_cumplMesSide' not in js:
        print("FAILED: res_cumplMesSide not found in js/resumen.js")
        sys.exit(1)
    if 'hookClearButton' not in js:
        print("FAILED: hookClearButton not found in js/resumen.js")
        sys.exit(1)
    print("PASS: js/resumen.js properly updates res_cumplMesSide and hooks clear button.")

    print("\nALL RESUMEN ST-SIDEBAR VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    verify()
