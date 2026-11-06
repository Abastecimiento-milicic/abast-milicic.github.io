import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_html = html.replace('20261106_112930', '20261106_114900')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated cache busters in index.html to 20261106_114900")

# Test syntax with node if available
try:
    res = subprocess.run(["node", "-c", "js/resumen.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("js/resumen.js syntax OK")
    else:
        print("js/resumen.js syntax error:", res.stderr)
except Exception as e:
    print("Node check error:", e)

try:
    res = subprocess.run(["node", "-c", "js/servicios.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("js/servicios.js syntax OK")
    else:
        print("js/servicios.js syntax error:", res.stderr)
except Exception as e:
    print("Node check error:", e)
