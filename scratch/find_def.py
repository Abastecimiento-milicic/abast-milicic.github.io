import os

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for file in files:
        if file.endswith('.js') or file.endswith('.html'):
            p = os.path.join(root, file)
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'syncAllStMultiSelects' in content:
                    print(f"{p}: has syncAllStMultiSelects")
