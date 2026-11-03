import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/resumen.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for l in lines:
    if 'cumplHeaders.find(h => /fecha/i.test(h))' in l:
        l = l.replace('cumplHeaders.find(h => /fecha/i.test(h))', 'cumplHeaders.find(h => /entrega\\s+esperada/i.test(h))')
        print("Replaced colFec")
    if 'ym === "2026-09"' in l:
        l = l.replace('ym === "2026-09"', 'ym === "2026-10"')
        print("Replaced default 2026-09 to 2026-10")
    if 'o.value === "2026-09"' in l:
        l = l.replace('o.value === "2026-09"', 'o.value === "2026-10"')
        print("Replaced option 2026-09 to 2026-10")
    if 'opt.value === "2026-09"' in l:
        l = l.replace('opt.value === "2026-09"', 'opt.value === "2026-10"')
        print("Replaced opt.value 2026-09 to 2026-10")
    new_lines.append(l)

with open("js/resumen.js", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Successfully written js/resumen.js")

# Bump cache buster to v82
with open("js/last-update.js", "r", encoding="utf-8") as f:
    lu = f.read()
lu = lu.replace("_v81_20261102_164500", "_v82_20261102_165500")
with open("js/last-update.js", "w", encoding="utf-8") as f:
    f.write(lu)

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()
idx = idx.replace("js/demoras.js?v=20261102_164500", "js/demoras.js?v=20261102_165500")
idx = idx.replace("js/resumen.js?v=20261102_164500", "js/resumen.js?v=20261102_165500")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("Bumped cache buster to v82")
