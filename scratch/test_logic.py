# Verify the logic for Nov 2026 onwards vs before Nov 2026

def calc_periodo_corto_nov2026(cd, c, d, isAftNov2026):
    muyCercana = None
    if isAftNov2026:
        # A PARTIR DE NOVIEMBRE 2026
        if cd in ["ZPOE", "ZPAS"]:
            if c == "00223" and d < 15: muyCercana = 1
            elif c == "00341" and d < 20: muyCercana = 1
            elif c == "00314" and d < 15: muyCercana = 1
            elif c == "00365" and d < 24: muyCercana = 1
            elif c == "00372" and d < 24: muyCercana = 1
            elif c == "00374" and d < 21: muyCercana = 1
            elif c == "00377" and d <= 22: muyCercana = 1
            elif c == "00378" and d < 15: muyCercana = 1
            elif c == "00379" and d < 12: muyCercana = 1
        elif cd in ["ZPAN", "ZPAI"]:
            if c == "00223" and d < 16: muyCercana = 1
            elif c == "00341" and d < 16: muyCercana = 1
            elif c == "00314" and d < 16: muyCercana = 1
            elif c == "00365" and d < 21: muyCercana = 1
            elif c == "00372" and d < 21: muyCercana = 1
            elif c == "00374" and d < 16: muyCercana = 1
            elif c == "00378" and d < 16: muyCercana = 1
            elif c == "00379" and d < 19: muyCercana = 1
            elif c == "00377" and d < 16: muyCercana = 1
    else:
        # ANTERIOR A NOVIEMBRE 2026
        if cd in ["ZPOE", "ZPAS"]:
            if c == "00038" and d <= 12: muyCercana = 1
            elif c == "00223" and d <= 15: muyCercana = 1
            elif c == "00357" and d < 5: muyCercana = 1
            elif c == "00359" and d < 5: muyCercana = 1
            elif c == "00341" and d <= 20: muyCercana = 1
            elif c == "00314" and d <= 15: muyCercana = 1
            elif c == "UTE 363" and d < 14: muyCercana = 1
            elif c == "00364" and d < 23: muyCercana = 1
            elif c == "00029MM" and d < 5: muyCercana = 1
            elif c == "00029MR" and d < 5: muyCercana = 1
            elif c == "00298" and d < 23: muyCercana = 1
            elif c == "00365" and d <= 19: muyCercana = 1
            elif c == "00367" and d < 25: muyCercana = 1
            elif c == "00369" and d < 16: muyCercana = 1
            elif c == "00371" and d < 12: muyCercana = 1
            elif c == "00372" and d <= 19: muyCercana = 1
            elif c == "00374" and d <= 21: muyCercana = 1
            elif c == "00375" and d < 14: muyCercana = 1
            elif c == "00376" and d <= 12: muyCercana = 1
            elif c == "00368" and d < 13: muyCercana = 1
            elif c == "00377" and d <= 22: muyCercana = 1
            elif c == "00378" and d <= 13: muyCercana = 1
            elif c == "00379" and d <= 12: muyCercana = 1
        elif cd in ["ZPAN", "ZPAI"]:
            if c == "00038" and d <= 8: muyCercana = 1
            elif c == "00223" and d <= 12: muyCercana = 1
            elif c == "00357" and d <= 5: muyCercana = 1
            elif c == "00359" and d <= 5: muyCercana = 1
            elif c == "00341" and d <= 17: muyCercana = 1
            elif c == "00314" and d <= 12: muyCercana = 1
            elif c == "UTE 363" and d <= 14: muyCercana = 1
            elif c == "00364" and d <= 19: muyCercana = 1
            elif c == "00029MM" and d <= 5: muyCercana = 1
            elif c == "00029MR" and d <= 5: muyCercana = 1
            elif c == "00298" and d <= 20: muyCercana = 1
            elif c == "00365" and d <= 16: muyCercana = 1
            elif c == "00367" and d <= 21: muyCercana = 1
            elif c == "00369" and d <= 12: muyCercana = 1
            elif c == "00371" and d <= 8: muyCercana = 1
            elif c == "00372" and d <= 16: muyCercana = 1
            elif c == "00374" and d <= 18: muyCercana = 1
            elif c == "00375" and d <= 11: muyCercana = 1
            elif c == "00378" and d <= 10: muyCercana = 1
            elif c == "00376" and d <= 9: muyCercana = 1
            elif c == "00379" and d <= 9: muyCercana = 1
            elif c == "00368" and d <= 10: muyCercana = 1
            elif c == "00377" and d <= 19: muyCercana = 1
    return muyCercana

# Tests
# 1. Nov 2026: c=00365, ZPOE, d=20 -> 1 (since < 24)
assert calc_periodo_corto_nov2026("ZPOE", "00365", 20, True) == 1
# 2. Before Nov 2026: c=00365, ZPOE, d=20 -> None (since <= 19)
assert calc_periodo_corto_nov2026("ZPOE", "00365", 20, False) is None

# 3. Nov 2026: c=00378, ZPAN, d=15 -> 1 (since < 16)
assert calc_periodo_corto_nov2026("ZPAN", "00378", 15, True) == 1
# 4. Before Nov 2026: c=00378, ZPAN, d=15 -> None (since <= 10)
assert calc_periodo_corto_nov2026("ZPAN", "00378", 15, False) is None

# 5. Nov 2026: c=00038, ZPOE, d=10 -> None (00038 removed from Nov 2026)
assert calc_periodo_corto_nov2026("ZPOE", "00038", 10, True) is None
# 6. Before Nov 2026: c=00038, ZPOE, d=10 -> 1 (since <= 12)
assert calc_periodo_corto_nov2026("ZPOE", "00038", 10, False) == 1

print("All tests passed with flying colors!")
