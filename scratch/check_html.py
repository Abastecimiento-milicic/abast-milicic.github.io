with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'id="panel-resumen"' in l:
        print(f"Found at line {i+1}")
        for j in range(max(0, i-5), min(len(lines), i+120)):
            print(f"{j+1}: {lines[j]}", end='')
        break
