with open('js/cumplimiento.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'exclude' in l.lower() or 'excluir' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
