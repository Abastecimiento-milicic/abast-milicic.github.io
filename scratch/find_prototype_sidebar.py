with open('prototipo_redisenio_180.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<aside' in l or 'app-sidebar' in l or 'filter-pill' in l or 'pills-container' in l:
        print(f"{i+1}: {l.strip()[:100]}")
