import sys
sys.stdout.reconfigure(encoding='utf-8')

# Update js/resumen.js
with open("js/resumen.js", "r", encoding="utf-8") as f:
    res = f.read()

res = res.replace("00026 / 00314 - CASA OLAVARRIA / SANTA FE", "00026 / 00314 - CASA OLAVARRIA")

# Ensure getCanonicalObraCode includes 0026 and 0314 explicitly
old_canon_res = 'if (c === "26" || c === "314" || c === "26_314" || c === "00026" || c === "00314") return "26_314";'
new_canon_res = 'if (c === "26" || c === "314" || c === "26_314" || c === "00026" || c === "00314" || c === "0026" || c === "0314") return "26_314";'
if old_canon_res in res:
    res = res.replace(old_canon_res, new_canon_res)

old_canon_35 = 'if (c === "35" || c === "341" || c === "35_341" || c === "00035" || c === "00341") return "35_341";'
new_canon_35 = 'if (c === "35" || c === "341" || c === "35_341" || c === "00035" || c === "00341" || c === "0035" || c === "0341") return "35_341";'
if old_canon_35 in res:
    res = res.replace(old_canon_35, new_canon_35)

with open("js/resumen.js", "w", encoding="utf-8") as f:
    f.write(res)
print("Updated js/resumen.js")

# Update js/demoras.js
with open("js/demoras.js", "r", encoding="utf-8") as f:
    dem = f.read()

if old_canon_res in dem:
    dem = dem.replace(old_canon_res, new_canon_res)
if old_canon_35 in dem:
    dem = dem.replace(old_canon_35, new_canon_35)

with open("js/demoras.js", "w", encoding="utf-8") as f:
    f.write(dem)
print("Updated js/demoras.js")
