with open('index.html', encoding='utf-8') as f:
    html = f.read()

assert 'height: 410px; min-height: 410px;' in html

with open('js/demoras.js', encoding='utf-8') as f:
    js = f.read()

assert js.count('orient: "horizontal"') >= 4, f"orient horizontal count: {js.count('orient: \"horizontal\"')}"
assert js.count('center: ["50%", "36%"]') >= 4, f"center count: {js.count('center: [\"50%\", \"36%\"]')}"
assert js.count('fontSize: 10.5') >= 4, f"fontSize count: {js.count('fontSize: 10.5')}"

print("All verifications passed 100%!")
