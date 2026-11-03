import os, sys
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    # skip .git
    if '.git' in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if '1500' in content:
                    lines = content.splitlines()
                    for idx, line in enumerate(lines):
                        if '1500' in line:
                            # if it's a huge CSV line, truncate
                            print(f"{filepath}:{idx+1}: {line.strip()[:150]}")
                            if filepath.endswith('.csv'):
                                break # just 1 sample from csv
        except Exception as e:
            pass
