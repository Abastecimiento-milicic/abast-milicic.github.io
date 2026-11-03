import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update js/demoras.js
with open('js/demoras.js', 'r', encoding='utf-8') as f:
    js_dem = f.read()

# 1.1 Update areaExplicacion formulas display
old_formula = """: areaName === 'PERIODO CORTO' ? `<b>Lógica de Cálculo PERIODO CORTO (Power Query M):</b>

FECHAENTREGAMUYCERCANA = let d = Duration.Days([FECHA ENTREGA ESPERADA] - [FECHA DE EMISION NECESIDAD]), c = Text.Trim(Text.From([CLI])) in
  if d = null then null
  else if List.Contains({"ZPOE","ZPAS"}, [CLASE DE DOC]) then
      if c="00038" and d<=12 then 1 else if c="00223" and d<=15 then 1 else if c="00357" and d<5 then 1 else if c="00359" and d<5 then 1
      else if c="00341" and d<=20 then 1 else if c="00314" and d<=15 then 1 else if c="UTE 363" and d<14 then 1 else if c="00364" and d<23 then 1
      else if c="00029MM" and d<5 then 1 else if c="00029MR" and d<5 then 1 else if c="00298" and d<23 then 1 else if c="00365" and d<=19 then 1
      else if c="00367" and d<25 then 1 else if c="00369" and d<16 then 1 else if c="00371" and d<12 then 1 else if c="00372" and d<=19 then 1
      else if c="00374" and d<=21 then 1 else if c="00375" and d<14 then 1 else if c="00376" and d<=12 then 1 else if c="00368" and d<13 then 1
      else if c="00377" and d<=22 then 1 else if c="00378" and d<=13 then 1 else if c="00379" and d<=12 then 1 else null
  else if List.Contains({"ZPAN","ZPAI"}, [CLASE DE DOC]) then
      if c="00038" and d<=8 then 1 else if c="00223" and d<=12 then 1 else if c="00357" and d<=5 then 1 else if c="00359" and d<=5 then 1
      else if c="00341" and d<=17 then 1 else if c="00314" and d<=12 then 1 else if c="UTE 363" and d<=14 then 1 else if c="00364" and d<=19 then 1
      else if c="00029MM" and d<=5 then 1 else if c="00029MR" and d<=5 then 1 else if c="00298" and d<=20 then 1 else if c="00365" and d<=16 then 1
      else if c="00367" and d<=21 then 1 else if c="00369" and d<=12 then 1 else if c="00371" and d<=8 then 1 else if c="00372" and d<=16 then 1
      else if c="00374" and d<=18 then 1 else if c="00375" and d<=11 then 1 else if c="00378" and d<=10 then 1 else if c="00376" and d<=9 then 1
      else if c="00379" and d<=9 then 1 else if c="00368" and d<=10 then 1 else if c="00377" and d<=19 then 1 else null
  else null

PERIODO CORTO = if [FECHAENTREGAMUYCERCANA] = 1 then 1 else null`"""

new_formula = """: areaName === 'PERIODO CORTO' ? `<b>Lógica de Cálculo PERIODO CORTO (Power Query M):</b>

<b>A partir de Noviembre 2026:</b>
FECHAENTREGAMUYCERCANA = let d = Duration.Days([FECHA ENTREGA ESPERADA] - [FECHA DE EMISION NECESIDAD]), c = Text.Trim(Text.From([CLI])) in
  if d = null then null
  else if List.Contains({"ZPOE","ZPAS"}, [CLASE DE DOC]) then
      if c="00223" and d<15 then 1 
      else if c="00341" and d<20 then 1 
      else if c="00314" and d<15 then 1 
      else if c="00365" and d<24 then 1
      else if c="00372" and d<24 then 1
      else if c="00374" and d<21 then 1 
      else if c="00377" and d<=22 then 1 
      else if c="00378" and d<15 then 1 
      else if c="00379" and d<12 then 1 else null
  else if List.Contains({"ZPAN","ZPAI"}, [CLASE DE DOC]) then
      if c="00223" and d<16 then 1 
      else if c="00341" and d<16 then 1 
      else if c="00314" and d<16 then 1 
      else if c="00365" and d<21 then 1
      else if c="00372" and d<21 then 1
      else if c="00374" and d<16 then 1 
      else if c="00378" and d<16 then 1 
      else if c="00379" and d<19 then 1 
      else if c="00377" and d<16 then 1 else null
  else null

<b>Anterior a Noviembre 2026 (Hasta Octubre 2026):</b>
FECHAENTREGAMUYCERCANA = let d = Duration.Days([FECHA ENTREGA ESPERADA] - [FECHA DE EMISION NECESIDAD]), c = Text.Trim(Text.From([CLI])) in
  if d = null then null
  else if List.Contains({"ZPOE","ZPAS"}, [CLASE DE DOC]) then
      if c="00038" and d<=12 then 1 else if c="00223" and d<=15 then 1 else if c="00357" and d<5 then 1 else if c="00359" and d<5 then 1
      else if c="00341" and d<=20 then 1 else if c="00314" and d<=15 then 1 else if c="UTE 363" and d<14 then 1 else if c="00364" and d<23 then 1
      else if c="00029MM" and d<5 then 1 else if c="00029MR" and d<5 then 1 else if c="00298" and d<23 then 1 else if c="00365" and d<=19 then 1
      else if c="00367" and d<25 then 1 else if c="00369" and d<16 then 1 else if c="00371" and d<12 then 1 else if c="00372" and d<=19 then 1
      else if c="00374" and d<=21 then 1 else if c="00375" and d<14 then 1 else if c="00376" and d<=12 then 1 else if c="00368" and d<13 then 1
      else if c="00377" and d<=22 then 1 else if c="00378" and d<=13 then 1 else if c="00379" and d<=12 then 1 else null
  else if List.Contains({"ZPAN","ZPAI"}, [CLASE DE DOC]) then
      if c="00038" and d<=8 then 1 else if c="00223" and d<=12 then 1 else if c="00357" and d<=5 then 1 else if c="00359" and d<=5 then 1
      else if c="00341" and d<=17 then 1 else if c="00314" and d<=12 then 1 else if c="UTE 363" and d<=14 then 1 else if c="00364" and d<=19 then 1
      else if c="00029MM" and d<=5 then 1 else if c="00029MR" and d<=5 then 1 else if c="00298" and d<=20 then 1 else if c="00365" and d<=16 then 1
      else if c="00367" and d<=21 then 1 else if c="00369" and d<=12 then 1 else if c="00371" and d<=8 then 1 else if c="00372" and d<=16 then 1
      else if c="00374" and d<=18 then 1 else if c="00375" and d<=11 then 1 else if c="00378" and d<=10 then 1 else if c="00376" and d<=9 then 1
      else if c="00379" and d<=9 then 1 else if c="00368" and d<=10 then 1 else if c="00377" and d<=19 then 1 else null
  else null

PERIODO CORTO = if [FECHAENTREGAMUYCERCANA] = 1 then 1 else null`"""

assert old_formula in js_dem, "old_formula not found in demoras.js"
js_dem = js_dem.replace(old_formula, new_formula, 1)

# 1.2 Update calculation in js/demoras.js
old_calc = """                    // FECHAENTREGAMUYCERCANA
                    let muyCercana = null;
                    if (fEntregaEsperada && fEmiNec) {
                      const d = daysBetween(fEmiNec, fEntregaEsperada);
                      const c = cli.toUpperCase();
                      if (["ZPOE","ZPAS"].includes(cd)) {
                        if (c === "00038" && d <= 12) muyCercana = 1;
                        else if (c === "00223" && d <= 15) muyCercana = 1;
                        else if (c === "00357" && d < 5) muyCercana = 1;
                        else if (c === "00359" && d < 5) muyCercana = 1;
                        else if (c === "00341" && d <= 20) muyCercana = 1;
                        else if (c === "00314" && d <= 15) muyCercana = 1;
                        else if (c === "UTE 363" && d < 14) muyCercana = 1;
                        else if (c === "00364" && d < 23) muyCercana = 1;
                        else if (c === "00029MM" && d < 5) muyCercana = 1;
                        else if (c === "00029MR" && d < 5) muyCercana = 1;
                        else if (c === "00298" && d < 23) muyCercana = 1;
                        else if (c === "00365" && d <= 19) muyCercana = 1;
                        else if (c === "00367" && d < 25) muyCercana = 1;
                        else if (c === "00369" && d < 16) muyCercana = 1;
                        else if (c === "00371" && d < 12) muyCercana = 1;
                        else if (c === "00372" && d <= 19) muyCercana = 1;
                        else if (c === "00374" && d <= 21) muyCercana = 1;
                        else if (c === "00375" && d < 14) muyCercana = 1;
                        else if (c === "00376" && d <= 12) muyCercana = 1;
                        else if (c === "00368" && d < 13) muyCercana = 1;
                        else if (c === "00377" && d <= 22) muyCercana = 1;
                        else if (c === "00378" && d <= 13) muyCercana = 1;
                        else if (c === "00379" && d <= 12) muyCercana = 1;
                      } else if (["ZPAN","ZPAI"].includes(cd)) {
                        if (c === "00038" && d <= 8) muyCercana = 1;
                        else if (c === "00223" && d <= 12) muyCercana = 1;
                        else if (c === "00357" && d <= 5) muyCercana = 1;
                        else if (c === "00359" && d <= 5) muyCercana = 1;
                        else if (c === "00341" && d <= 17) muyCercana = 1;
                        else if (c === "00314" && d <= 12) muyCercana = 1;
                        else if (c === "UTE 363" && d <= 14) muyCercana = 1;
                        else if (c === "00364" && d <= 19) muyCercana = 1;
                        else if (c === "00029MM" && d <= 5) muyCercana = 1;
                        else if (c === "00029MR" && d <= 5) muyCercana = 1;
                        else if (c === "00298" && d <= 20) muyCercana = 1;
                        else if (c === "00365" && d <= 16) muyCercana = 1;
                        else if (c === "00367" && d <= 21) muyCercana = 1;
                        else if (c === "00369" && d <= 12) muyCercana = 1;
                        else if (c === "00371" && d <= 8) muyCercana = 1;
                        else if (c === "00372" && d <= 16) muyCercana = 1;
                        else if (c === "00374" && d <= 18) muyCercana = 1;
                        else if (c === "00375" && d <= 11) muyCercana = 1;
                        else if (c === "00378" && d <= 10) muyCercana = 1;
                        else if (c === "00376" && d <= 9) muyCercana = 1;
                        else if (c === "00379" && d <= 9) muyCercana = 1;
                        else if (c === "00368" && d <= 10) muyCercana = 1;
                        else if (c === "00377" && d <= 19) muyCercana = 1;
                      }
                    }
                    r["FECHAENTREGAMUYCERCANA"] = muyCercana;"""

new_calc = """                    // FECHAENTREGAMUYCERCANA
                    let muyCercana = null;
                    if (fEntregaEsperada && fEmiNec) {
                      const d = daysBetween(fEmiNec, fEntregaEsperada);
                      const c = cli.toUpperCase();
                      const isAftNov2026 = (fEntregaEsperada >= new Date(2026, 10, 1));

                      if (isAftNov2026) {
                        // A PARTIR DE NOVIEMBRE 2026
                        if (["ZPOE","ZPAS"].includes(cd)) {
                          if (c === "00223" && d < 15) muyCercana = 1;
                          else if (c === "00341" && d < 20) muyCercana = 1;
                          else if (c === "00314" && d < 15) muyCercana = 1;
                          else if (c === "00365" && d < 24) muyCercana = 1;
                          else if (c === "00372" && d < 24) muyCercana = 1;
                          else if (c === "00374" && d < 21) muyCercana = 1;
                          else if (c === "00377" && d <= 22) muyCercana = 1;
                          else if (c === "00378" && d < 15) muyCercana = 1;
                          else if (c === "00379" && d < 12) muyCercana = 1;
                        } else if (["ZPAN","ZPAI"].includes(cd)) {
                          if (c === "00223" && d < 16) muyCercana = 1;
                          else if (c === "00341" && d < 16) muyCercana = 1;
                          else if (c === "00314" && d < 16) muyCercana = 1;
                          else if (c === "00365" && d < 21) muyCercana = 1;
                          else if (c === "00372" && d < 21) muyCercana = 1;
                          else if (c === "00374" && d < 16) muyCercana = 1;
                          else if (c === "00378" && d < 16) muyCercana = 1;
                          else if (c === "00379" && d < 19) muyCercana = 1;
                          else if (c === "00377" && d < 16) muyCercana = 1;
                        }
                      } else {
                        // ANTERIOR A NOVIEMBRE 2026 (REGLAS VIGENTES HASTA OCTUBRE 2026)
                        if (["ZPOE","ZPAS"].includes(cd)) {
                          if (c === "00038" && d <= 12) muyCercana = 1;
                          else if (c === "00223" && d <= 15) muyCercana = 1;
                          else if (c === "00357" && d < 5) muyCercana = 1;
                          else if (c === "00359" && d < 5) muyCercana = 1;
                          else if (c === "00341" && d <= 20) muyCercana = 1;
                          else if (c === "00314" && d <= 15) muyCercana = 1;
                          else if (c === "UTE 363" && d < 14) muyCercana = 1;
                          else if (c === "00364" && d < 23) muyCercana = 1;
                          else if (c === "00029MM" && d < 5) muyCercana = 1;
                          else if (c === "00029MR" && d < 5) muyCercana = 1;
                          else if (c === "00298" && d < 23) muyCercana = 1;
                          else if (c === "00365" && d <= 19) muyCercana = 1;
                          else if (c === "00367" && d < 25) muyCercana = 1;
                          else if (c === "00369" && d < 16) muyCercana = 1;
                          else if (c === "00371" && d < 12) muyCercana = 1;
                          else if (c === "00372" && d <= 19) muyCercana = 1;
                          else if (c === "00374" && d <= 21) muyCercana = 1;
                          else if (c === "00375" && d < 14) muyCercana = 1;
                          else if (c === "00376" && d <= 12) muyCercana = 1;
                          else if (c === "00368" && d < 13) muyCercana = 1;
                          else if (c === "00377" && d <= 22) muyCercana = 1;
                          else if (c === "00378" && d <= 13) muyCercana = 1;
                          else if (c === "00379" && d <= 12) muyCercana = 1;
                        } else if (["ZPAN","ZPAI"].includes(cd)) {
                          if (c === "00038" && d <= 8) muyCercana = 1;
                          else if (c === "00223" && d <= 12) muyCercana = 1;
                          else if (c === "00357" && d <= 5) muyCercana = 1;
                          else if (c === "00359" && d <= 5) muyCercana = 1;
                          else if (c === "00341" && d <= 17) muyCercana = 1;
                          else if (c === "00314" && d <= 12) muyCercana = 1;
                          else if (c === "UTE 363" && d <= 14) muyCercana = 1;
                          else if (c === "00364" && d <= 19) muyCercana = 1;
                          else if (c === "00029MM" && d <= 5) muyCercana = 1;
                          else if (c === "00029MR" && d <= 5) muyCercana = 1;
                          else if (c === "00298" && d <= 20) muyCercana = 1;
                          else if (c === "00365" && d <= 16) muyCercana = 1;
                          else if (c === "00367" && d <= 21) muyCercana = 1;
                          else if (c === "00369" && d <= 12) muyCercana = 1;
                          else if (c === "00371" && d <= 8) muyCercana = 1;
                          else if (c === "00372" && d <= 16) muyCercana = 1;
                          else if (c === "00374" && d <= 18) muyCercana = 1;
                          else if (c === "00375" && d <= 11) muyCercana = 1;
                          else if (c === "00378" && d <= 10) muyCercana = 1;
                          else if (c === "00376" && d <= 9) muyCercana = 1;
                          else if (c === "00379" && d <= 9) muyCercana = 1;
                          else if (c === "00368" && d <= 10) muyCercana = 1;
                          else if (c === "00377" && d <= 19) muyCercana = 1;
                        }
                      }
                    }
                    r["FECHAENTREGAMUYCERCANA"] = muyCercana;"""

assert old_calc in js_dem, "old_calc not found in demoras.js"
js_dem = js_dem.replace(old_calc, new_calc, 1)

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(js_dem)

print("Updated js/demoras.js successfully!")

# 2. Update js/clasificacion_logic.js
with open('js/clasificacion_logic.js', 'r', encoding='utf-8') as f:
    js_clas = f.read()

old_clas_calc = """                  // FECHAENTREGAMUYCERCANA
                  var dExpEmis = null;
                  if (dtEntregaEsperada && dtEmisionNecesidad) dExpEmis = diffDays(dtEntregaEsperada, dtEmisionNecesidad);
                  var muyCercana = null;
                  if (dExpEmis !== null) {
                      if (["ZPOE","ZPAS"].includes(claseDoc)) {
                          if (c === "00038" && dExpEmis <= 12) muyCercana = 1;
                          else if (c === "00223" && dExpEmis <= 15) muyCercana = 1;
                          else if (c === "00357" && dExpEmis < 5) muyCercana = 1;
                          else if (c === "00359" && dExpEmis < 5) muyCercana = 1;
                          else if (c === "00341" && dExpEmis <= 20) muyCercana = 1;
                          else if (c === "00314" && dExpEmis <= 15) muyCercana = 1;
                          else if (c === "UTE 363" && dExpEmis < 14) muyCercana = 1;
                          else if (c === "00364" && dExpEmis < 23) muyCercana = 1;
                          else if (c === "00029MM" && dExpEmis < 5) muyCercana = 1;
                          else if (c === "00029MR" && dExpEmis < 5) muyCercana = 1;
                          else if (c === "00298" && dExpEmis < 23) muyCercana = 1;
                          else if (c === "00365" && dExpEmis <= 19) muyCercana = 1;
                          else if (c === "00367" && dExpEmis < 25) muyCercana = 1;
                          else if (c === "00369" && dExpEmis < 16) muyCercana = 1;
                          else if (c === "00371" && dExpEmis < 12) muyCercana = 1;
                          else if (c === "00372" && dExpEmis <= 19) muyCercana = 1;
                          else if (c === "00374" && dExpEmis <= 21) muyCercana = 1;
                          else if (c === "00375" && dExpEmis < 14) muyCercana = 1;
                          else if (c === "00376" && dExpEmis <= 12) muyCercana = 1;
                          else if (c === "00368" && dExpEmis < 13) muyCercana = 1;
                          else if (c === "00377" && dExpEmis <= 22) muyCercana = 1;
                          else if (c === "00378" && dExpEmis <= 13) muyCercana = 1;
                          else if (c === "00379" && dExpEmis <= 12) muyCercana = 1;
                      } else if (["ZPAN","ZPAI"].includes(claseDoc)) {
                          if (c === "00038" && dExpEmis <= 8) muyCercana = 1;
                          else if (c === "00223" && dExpEmis <= 12) muyCercana = 1;
                          else if (c === "00357" && dExpEmis <= 5) muyCercana = 1;
                          else if (c === "00359" && dExpEmis <= 5) muyCercana = 1;
                          else if (c === "00341" && dExpEmis <= 17) muyCercana = 1;
                          else if (c === "00314" && dExpEmis <= 12) muyCercana = 1;
                          else if (c === "UTE 363" && dExpEmis <= 14) muyCercana = 1;
                          else if (c === "00364" && dExpEmis <= 19) muyCercana = 1;
                          else if (c === "00029MM" && dExpEmis <= 5) muyCercana = 1;
                          else if (c === "00029MR" && dExpEmis <= 5) muyCercana = 1;
                          else if (c === "00298" && dExpEmis <= 20) muyCercana = 1;
                          else if (c === "00365" && dExpEmis <= 16) muyCercana = 1;
                          else if (c === "00367" && dExpEmis <= 21) muyCercana = 1;
                          else if (c === "00369" && dExpEmis <= 12) muyCercana = 1;
                          else if (c === "00371" && dExpEmis <= 8) muyCercana = 1;
                          else if (c === "00372" && dExpEmis <= 16) muyCercana = 1;
                          else if (c === "00374" && dExpEmis <= 18) muyCercana = 1;
                          else if (c === "00375" && dExpEmis <= 11) muyCercana = 1;
                          else if (c === "00378" && dExpEmis <= 10) muyCercana = 1;
                          else if (c === "00376" && dExpEmis <= 9) muyCercana = 1;
                          else if (c === "00379" && dExpEmis <= 9) muyCercana = 1;
                          else if (c === "00368" && dExpEmis <= 10) muyCercana = 1;
                          else if (c === "00377" && dExpEmis <= 19) muyCercana = 1;
                      }
                  }
                  o["FECHAENTREGAMUYCERCANA"] = muyCercana;"""

new_clas_calc = """                  // FECHAENTREGAMUYCERCANA
                  var dExpEmis = null;
                  if (dtEntregaEsperada && dtEmisionNecesidad) dExpEmis = diffDays(dtEntregaEsperada, dtEmisionNecesidad);
                  var muyCercana = null;
                  if (dExpEmis !== null) {
                      var isAftNov2026 = (dtEntregaEsperada >= new Date(2026, 10, 1));
                      if (isAftNov2026) {
                          // A PARTIR DE NOVIEMBRE 2026
                          if (["ZPOE","ZPAS"].includes(claseDoc)) {
                              if (c === "00223" && dExpEmis < 15) muyCercana = 1;
                              else if (c === "00341" && dExpEmis < 20) muyCercana = 1;
                              else if (c === "00314" && dExpEmis < 15) muyCercana = 1;
                              else if (c === "00365" && dExpEmis < 24) muyCercana = 1;
                              else if (c === "00372" && dExpEmis < 24) muyCercana = 1;
                              else if (c === "00374" && dExpEmis < 21) muyCercana = 1;
                              else if (c === "00377" && dExpEmis <= 22) muyCercana = 1;
                              else if (c === "00378" && dExpEmis < 15) muyCercana = 1;
                              else if (c === "00379" && dExpEmis < 12) muyCercana = 1;
                          } else if (["ZPAN","ZPAI"].includes(claseDoc)) {
                              if (c === "00223" && dExpEmis < 16) muyCercana = 1;
                              else if (c === "00341" && dExpEmis < 16) muyCercana = 1;
                              else if (c === "00314" && dExpEmis < 16) muyCercana = 1;
                              else if (c === "00365" && dExpEmis < 21) muyCercana = 1;
                              else if (c === "00372" && dExpEmis < 21) muyCercana = 1;
                              else if (c === "00374" && dExpEmis < 16) muyCercana = 1;
                              else if (c === "00378" && dExpEmis < 16) muyCercana = 1;
                              else if (c === "00379" && dExpEmis < 19) muyCercana = 1;
                              else if (c === "00377" && dExpEmis < 16) muyCercana = 1;
                          }
                      } else {
                          // ANTERIOR A NOVIEMBRE 2026
                          if (["ZPOE","ZPAS"].includes(claseDoc)) {
                              if (c === "00038" && dExpEmis <= 12) muyCercana = 1;
                              else if (c === "00223" && dExpEmis <= 15) muyCercana = 1;
                              else if (c === "00357" && dExpEmis < 5) muyCercana = 1;
                              else if (c === "00359" && dExpEmis < 5) muyCercana = 1;
                              else if (c === "00341" && dExpEmis <= 20) muyCercana = 1;
                              else if (c === "00314" && dExpEmis <= 15) muyCercana = 1;
                              else if (c === "UTE 363" && dExpEmis < 14) muyCercana = 1;
                              else if (c === "00364" && dExpEmis < 23) muyCercana = 1;
                              else if (c === "00029MM" && dExpEmis < 5) muyCercana = 1;
                              else if (c === "00029MR" && dExpEmis < 5) muyCercana = 1;
                              else if (c === "00298" && dExpEmis < 23) muyCercana = 1;
                              else if (c === "00365" && dExpEmis <= 19) muyCercana = 1;
                              else if (c === "00367" && dExpEmis < 25) muyCercana = 1;
                              else if (c === "00369" && dExpEmis < 16) muyCercana = 1;
                              else if (c === "00371" && dExpEmis < 12) muyCercana = 1;
                              else if (c === "00372" && dExpEmis <= 19) muyCercana = 1;
                              else if (c === "00374" && dExpEmis <= 21) muyCercana = 1;
                              else if (c === "00375" && dExpEmis < 14) muyCercana = 1;
                              else if (c === "00376" && dExpEmis <= 12) muyCercana = 1;
                              else if (c === "00368" && dExpEmis < 13) muyCercana = 1;
                              else if (c === "00377" && dExpEmis <= 22) muyCercana = 1;
                              else if (c === "00378" && dExpEmis <= 13) muyCercana = 1;
                              else if (c === "00379" && dExpEmis <= 12) muyCercana = 1;
                          } else if (["ZPAN","ZPAI"].includes(claseDoc)) {
                              if (c === "00038" && dExpEmis <= 8) muyCercana = 1;
                              else if (c === "00223" && dExpEmis <= 12) muyCercana = 1;
                              else if (c === "00357" && dExpEmis <= 5) muyCercana = 1;
                              else if (c === "00359" && dExpEmis <= 5) muyCercana = 1;
                              else if (c === "00341" && dExpEmis <= 17) muyCercana = 1;
                              else if (c === "00314" && dExpEmis <= 12) muyCercana = 1;
                              else if (c === "UTE 363" && dExpEmis <= 14) muyCercana = 1;
                              else if (c === "00364" && dExpEmis <= 19) muyCercana = 1;
                              else if (c === "00029MM" && dExpEmis <= 5) muyCercana = 1;
                              else if (c === "00029MR" && dExpEmis <= 5) muyCercana = 1;
                              else if (c === "00298" && dExpEmis <= 20) muyCercana = 1;
                              else if (c === "00365" && dExpEmis <= 16) muyCercana = 1;
                              else if (c === "00367" && dExpEmis <= 21) muyCercana = 1;
                              else if (c === "00369" && dExpEmis <= 12) muyCercana = 1;
                              else if (c === "00371" && dExpEmis <= 8) muyCercana = 1;
                              else if (c === "00372" && dExpEmis <= 16) muyCercana = 1;
                              else if (c === "00374" && dExpEmis <= 18) muyCercana = 1;
                              else if (c === "00375" && dExpEmis <= 11) muyCercana = 1;
                              else if (c === "00378" && dExpEmis <= 10) muyCercana = 1;
                              else if (c === "00376" && dExpEmis <= 9) muyCercana = 1;
                              else if (c === "00379" && dExpEmis <= 9) muyCercana = 1;
                              else if (c === "00368" && dExpEmis <= 10) muyCercana = 1;
                              else if (c === "00377" && dExpEmis <= 19) muyCercana = 1;
                          }
                      }
                  }
                  o["FECHAENTREGAMUYCERCANA"] = muyCercana;"""

assert old_clas_calc in js_clas, "old_clas_calc not found in clasificacion_logic.js"
js_clas = js_clas.replace(old_clas_calc, new_clas_calc, 1)

with open('js/clasificacion_logic.js', 'w', encoding='utf-8') as f:
    f.write(js_clas)

print("Updated js/clasificacion_logic.js successfully!")

# 3. Bump CACHE_BUSTER in js/last-update.js
with open('js/last-update.js', 'r', encoding='utf-8') as f:
    js_lu = f.read()

old_cb = 'window.CACHE_BUSTER = cb + "_v76_20261021_145300";'
new_cb = 'window.CACHE_BUSTER = cb + "_v77_20261102_150000";'

assert old_cb in js_lu, "old_cb not found in last-update.js"
js_lu = js_lu.replace(old_cb, new_cb, 1)

with open('js/last-update.js', 'w', encoding='utf-8') as f:
    f.write(js_lu)

print("Updated js/last-update.js CACHE_BUSTER successfully!")

# 4. Bump cache busters in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('?v=20261102_144500', '?v=20261102_150000')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html cache buster successfully!")
