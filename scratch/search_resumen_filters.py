with open('js/resumen.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['populateObraSelect', 'populateAnio', 'populateMes', 'getSelectedObras', 'btnClearFilters', 'btnArriba', 'lblObra', 'isResumenArribaActive', 'switchArriba']):
        print(f"{i+1}: {l.strip()[:100]}")
