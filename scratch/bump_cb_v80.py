import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/last-update.js", "r", encoding="utf-8") as f:
    lu = f.read()

lu = lu.replace("_v79_20261102_153500", "_v80_20261102_155200")

with open("js/last-update.js", "w", encoding="utf-8") as f:
    f.write(lu)

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

idx = idx.replace("js/demoras.js?v=20261102_153500", "js/demoras.js?v=20261102_155200")
idx = idx.replace("js/resumen.js?v=20261102_153500", "js/resumen.js?v=20261102_155200")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("Bumped cache buster to v80")
