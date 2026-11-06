with open('css/base.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines[-80:]):
    print(f"{len(lines)-80+i+1}: {l.strip()[:100]}")
