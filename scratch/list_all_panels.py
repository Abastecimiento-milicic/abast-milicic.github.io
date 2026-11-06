import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

panels = []
current_panel = None
for i, line in enumerate(lines):
    if '<section id="panel-' in line or '<div id="panel-' in line:
        current_panel = line.strip()
        panels.append((i+1, current_panel))
    elif '<aside class="st-sidebar' in line:
        print(f"Line {i+1} in {current_panel}: {line.strip()}")

print("\n--- All Panels Found ---")
for p in panels:
    print(p)
