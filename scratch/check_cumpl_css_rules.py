import sys
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['index.html', 'css/base.css']:
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"=== {fn} (cumpl-) ===")
    for i, l in enumerate(lines):
        if 'cumpl-' in l and ('{' in l or 'color' in l):
            print(f"  {i+1}: {l.strip()}")
            for j in range(i+1, min(len(lines), i+8)):
                print(f"      {j+1}: {lines[j].strip()}")
                if '}' in lines[j]: break
