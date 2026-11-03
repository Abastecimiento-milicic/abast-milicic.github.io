import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

selects = re.findall(r'<select[^>]*id="([^"]+)"[^>]*>', text)
print("Select IDs in index.html:")
for s in selects:
    print(" ", s)
