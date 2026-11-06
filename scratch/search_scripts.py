with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.js?v=' in l or '.css?v=' in l or 'CACHE_BUSTER' in l:
        print(f"{i+1}: {l.strip()}")
