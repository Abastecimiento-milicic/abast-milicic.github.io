with open('css/base.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'pills-container' in l or 'filter-pill' in l or 'toggle-row' in l or 'switch-ui' in l or 'panel-servicios' in l:
        print(f"{i+1}: {l.strip()[:100]}")
