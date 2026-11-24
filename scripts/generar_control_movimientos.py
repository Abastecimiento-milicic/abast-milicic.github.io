# -*- coding: utf-8 -*-
"""
Generador de datos para Control de Movimientos MB51
Procesa MB51 2025.xlsx y MB51 2026.xlsx y genera data/control_movimientos_mb51.json
con los usuarios únicos que operaron por mes, año, almacén, CMv y centro.
"""

import os
import sys
import json
import datetime
import openpyxl

def norm_almacen(v):
    if v is None:
        return "(Sin Almacen)"
    s = str(v).strip().replace('.0', '').upper()
    if not s or s == 'NONE' or s == 'NAN':
        return "(Sin Almacen)"
    # Si es numérico de 1 a 3 dígitos, rellenar con ceros a la izquierda (ej: 223 -> 0223, 26 -> 0026)
    if s.isdigit() and len(s) < 4:
        s = s.zfill(4)
    return s

def norm_cmv(v):
    if v is None:
        return "-"
    s = str(v).strip().replace('.0', '')
    return s if s else "-"

def norm_text(v):
    if v is None:
        return ""
    s = str(v).strip().replace('.0', '').upper()
    return "" if s in ('NONE', 'NAN') else s

def extract_year_month(fe, default_year=2025):
    if not fe:
        return None, None
    if hasattr(fe, 'year') and hasattr(fe, 'month'):
        return int(fe.year), int(fe.month)
    s = str(fe).strip()[:10]
    # formato YYYY-MM-DD o DD/MM/YYYY
    if '-' in s:
        p = s.split('-')
        if len(p) >= 3:
            try:
                y = int(p[0])
                m = int(p[1])
                return y, m
            except Exception:
                pass
    elif '/' in s:
        p = s.split('/')
        if len(p) >= 3:
            try:
                # Si el primer elemento tiene 4 dígitos -> YYYY/MM/DD
                if len(p[0]) == 4:
                    return int(p[0]), int(p[1])
                # Sino DD/MM/YYYY
                return int(p[2]), int(p[1])
            except Exception:
                pass
    return None, None

def generate_control_movimientos(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    data_dir = os.path.join(base_dir, 'data')
    out_json = os.path.join(data_dir, 'control_movimientos_mb51.json')

    files = [
        ('MB51 2025.xlsx', 2025),
        ('MB51 2026.xlsx', 2026)
    ]

    print("=" * 70)
    print("      CONSOLIDADOR DE CONTROL DE MOVIMIENTOS MB51 (SAP)")
    print("=" * 70)
    print(f"Directorio de datos : {data_dir}")
    print(f"Archivo de salida   : {out_json}")
    print("-" * 70)

    # Agrupador: (y, m, cnt, alm, cmv) -> { "users": set(), "count": int }
    groups = {}
    unique_almacenes = set()
    unique_cmvs = set()
    unique_centros = set()
    unique_users = set()
    unique_years = set()
    total_rows = 0

    for fname, default_year in files:
        fpath = os.path.join(data_dir, fname)
        if not os.path.exists(fpath):
            print(f"[AVISO] No se encontró {fname}, omitiendo...")
            continue

        print(f"\nProcesando {fname} ...")
        wb = openpyxl.load_workbook(fpath, read_only=True)
        ws = wb.active

        # Mapear columnas
        header_row = next(ws.iter_rows(max_row=1))
        headers = [str(c.value or '').strip() for c in header_row]
        h_idx = {}
        for idx, h in enumerate(headers):
            h_clean = h.lower()
            if 'almac' in h_clean:
                h_idx['alm'] = idx
            elif 'clase' in h_clean and 'mov' in h_clean:
                h_idx['cmv'] = idx
            elif 'centro' in h_clean and 'coste' not in h_clean:
                h_idx['cnt'] = idx
            elif 'usuario' in h_clean:
                h_idx['user'] = idx
            elif 'contabiliz' in h_clean:
                h_idx['fe'] = idx

        c_alm = h_idx.get('alm')
        c_cmv = h_idx.get('cmv')
        c_cnt = h_idx.get('cnt')
        c_user = h_idx.get('user')
        c_fe = h_idx.get('fe')

        if c_fe is None or c_user is None:
            print(f"  [ERROR] Faltan columnas críticas en {fname}. Headers encontrados: {headers}")
            wb.close()
            continue

        file_rows = 0
        valid_rows = 0

        for row in ws.iter_rows(min_row=2, values_only=True):
            file_rows += 1
            user = norm_text(row[c_user])
            if not user:
                continue

            fe_val = row[c_fe]
            y, m = extract_year_month(fe_val, default_year)
            if not y or not m or not (2020 <= y <= 2035) or not (1 <= m <= 12):
                y = default_year
                m = 1 if not m else m

            alm = norm_almacen(row[c_alm]) if c_alm is not None else "(Sin Almacen)"
            cmv = norm_cmv(row[c_cmv]) if c_cmv is not None else "-"
            cnt = norm_text(row[c_cnt]) if c_cnt is not None else "MR01"
            if not cnt:
                cnt = "MR01"

            k = (y, m, cnt, alm, cmv)
            if k not in groups:
                groups[k] = {"u": set(), "c": 0}
            groups[k]["u"].add(user)
            groups[k]["c"] += 1

            unique_almacenes.add(alm)
            unique_cmvs.add(cmv)
            unique_centros.add(cnt)
            unique_users.add(user)
            unique_years.add(y)
            valid_rows += 1

            if file_rows % 150000 == 0:
                print(f"  -> {file_rows:,d} filas leídas ({valid_rows:,d} válidas)...")

        wb.close()
        total_rows += file_rows
        print(f"  Finalizado {fname}: {file_rows:,d} filas procesadas.")

    print("\nConstruyendo estructura JSON compacta...")
    records = []
    for (y, m, cnt, alm, cmv), d in groups.items():
        records.append({
            "y": y,
            "m": m,
            "cnt": cnt,
            "alm": alm,
            "cmv": cmv,
            "u": sorted(list(d["u"])),
            "c": d["c"]
        })

    # Ordenar por año, mes, almacén, cmv
    records.sort(key=lambda x: (x["y"], x["m"], x["alm"], x["cmv"]))

    payload = {
        "generated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total_source_rows": total_rows,
        "total_groups": len(records),
        "years": sorted(list(unique_years)),
        "centros": sorted(list(unique_centros)),
        "almacenes": sorted(list(unique_almacenes), key=lambda x: (x == "(Sin Almacen)", x)),
        "cmvs": sorted(list(unique_cmvs)),
        "users": sorted(list(unique_users)),
        "records": records
    }

    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)

    size_mb = os.path.getsize(out_json) / (1024 * 1024)
    print("=" * 70)
    print(f"RESULTADO EXITOSO:")
    print(f"  Total transacciones MB51 procesadas : {total_rows:,d}")
    print(f"  Grupos agregados (Mes/Alm/CMv)      : {len(records):,d}")
    print(f"  Almacenes únicos detectados         : {len(unique_almacenes)}")
    print(f"  Clases de movimiento (CMv) únicas  : {len(unique_cmvs)}")
    print(f"  Usuarios únicos detectados          : {len(unique_users)}")
    print(f"  Tamaño archivo JSON generado        : {size_mb:.2f} MB")
    print(f"  Destino                             : {out_json}")
    print("=" * 70)

if __name__ == '__main__':
    generate_control_movimientos()
