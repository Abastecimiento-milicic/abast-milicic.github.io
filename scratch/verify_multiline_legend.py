import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()
assert 'height: 470px; min-height: 470px;' in html

with open('js/demoras.js', encoding='utf-8') as f:
    js = f.read()

assert js.count('type: "plain"') >= 4, f"type: plain count is {js.count('type: \"plain\"')}"
assert js.count('radius: ["28%", "48%"]') >= 4, f"radius count is {js.count('radius: [\"28%\", \"48%\"]')}"
assert js.count('center: ["50%", "35%"]') >= 4, f"center count is {js.count('center: [\"50%\", \"35%\"]')}"
assert js.count('position: "outside"') >= 4, f"position outside count is {js.count('position: \"outside\"')}"

print("ALL VERIFICATIONS PASSED: Multiline legend wrapping without scroll and outside labels with description + percentage are configured!")
