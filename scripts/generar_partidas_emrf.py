import os
import sys
import json
import unicodedata
import datetime
import numpy as np
import pandas as pd

# Importar generador de partidas abiertas
try:
    from generar_partidas_abiertas import build_partidas_abiertas
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)
    from generar_partidas_abiertas import build_partidas_abiertas

def clean_col(c):
    nfkd = unicodedata.normalize('NFKD', str(c))
    return ''.join([ch for ch in nfkd if not unicodedata.combining(ch)]).lower().strip()

def get_default_corte():
    try:
        last_update_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "js", "last-update.js")
        if os.path.exists(last_update_path):
            with open(last_update_path, "r", encoding="utf-8") as f:
                import re
                m = re.search(r'LAST_UPDATE\s*=\s*["\']([^"\']+)["\']', f.read())
                if m:
                    return m.group(1).strip()
    except Exception:
        pass
    return datetime.datetime.now().strftime("%d/%m/%Y")

def process_data(data_dir=None, corte_str=None):
    if corte_str is None:
        corte_str = get_default_corte()
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop", "PARTIDAS ABIERTAS")

    # 1. Asegurar la generación/actualización de Partidas abiertas
    partidas_xlsx = os.path.join(data_dir, "Partidas abiertas.xlsx")
    partidas_csv = os.path.join(data_dir, "Partidas abiertas.csv")

    try:
        # Si no existe o si los archivos base están presentes y son más recientes
        needs_build = not os.path.exists(partidas_xlsx)
        for base_name in ['FBL3N.xlsx', 'ME2L.xlsx', 'Z909.xlsx']:
            for cand_dir in [data_dir, desktop_dir]:
                bp = os.path.join(cand_dir, base_name)
                if os.path.exists(bp):
                    if not os.path.exists(partidas_xlsx) or os.path.getmtime(bp) > os.path.getmtime(partidas_xlsx):
                        needs_build = True
                        break

        if needs_build:
            print("Generando archivo consolidado 'Partidas abiertas' desde FBL3N, ME2L y Z909...")
            build_partidas_abiertas(custom_dir=data_dir, verbose=False)
    except Exception as e:
        print(f"[WARN] Error al verificar/generar Partidas abiertas: {e}")

    # 2. Cargar 'Partidas abiertas'
    raw = None
    if os.path.exists(partidas_csv):
        try:
            print(f"Cargando {partidas_csv}...")
            raw = pd.read_csv(partidas_csv, encoding='utf-8', low_memory=False)
        except Exception:
            raw = None

    if raw is None and os.path.exists(partidas_xlsx):
        print(f"Cargando {partidas_xlsx}...")
        raw = pd.read_excel(partidas_xlsx, sheet_name='Data')

    if raw is None or raw.empty:
        # Fallback a Desktop si no estaba en data_dir
        desktop_xlsx = os.path.join(desktop_dir, "Partidas abiertas.xlsx")
        if os.path.exists(desktop_xlsx):
            print(f"Cargando desde Desktop: {desktop_xlsx}...")
            raw = pd.read_excel(desktop_xlsx, sheet_name='Data')

    if raw is None or raw.empty:
        print("[ERROR] No se pudo cargar el archivo 'Partidas abiertas'.")
        return

    # Cargar mapeo de operadores si existe
    op_map = {}
    for map_dir in [data_dir, desktop_dir]:
        map_path = os.path.join(map_dir, 'operadores_map.json')
        if os.path.exists(map_path):
            try:
                with open(map_path, 'r', encoding='utf-8') as f_op:
                    op_map.update(json.load(f_op))
            except Exception as e:
                print(f"Error al cargar operadores_map.json: {e}")

    # Renombrar columnas a formato limpio
    raw = raw.rename(columns={c: clean_col(c) for c in raw.columns})

    # Filtrar filas de totales o vacías en columnas clave
    key_cols = [k for k in ['documento compras', 'posicion', 'clave contabiliz.'] if k in raw.columns]
    if key_cols:
        raw = raw.dropna(subset=key_cols).copy()

    # Mapear Sociedad
    if 'sociedad' in raw.columns:
        raw['Sociedad'] = raw['sociedad'].astype(str).str.strip()
    else:
        raw['Sociedad'] = 'MLAR'

    raw['Pedido'] = raw['documento compras'].astype(np.int64).astype(str)
    raw['Posicion'] = raw['posicion'].astype(int).astype(str)
    raw['Key'] = raw['Sociedad'] + '_' + raw['Pedido'] + '_' + raw['Posicion']

    raw['Importe'] = pd.to_numeric(raw['importe en moneda local'], errors='coerce').fillna(0.0)
    raw['Moneda'] = raw.get('moneda local', pd.Series('ARS', index=raw.index)).fillna('ARS')

    raw['Clave_Contab'] = raw['clave contabiliz.'].astype(int).astype(str)
    raw['Clase_Doc'] = raw.get('clase de documento', pd.Series('', index=raw.index)).fillna('').astype(str).str.strip()
    raw['Doc_SAP'] = raw.get('no documento', pd.Series('', index=raw.index)).fillna(0).astype(np.int64).astype(str)

    raw['Fecha_Doc'] = pd.to_datetime(raw.get('fecha de documento'), errors='coerce', dayfirst=True)
    raw['Fe_Contabilizacion'] = pd.to_datetime(
        raw.get('fe.contabilizacion', raw.get('fecha de contabilizacion', pd.Series(pd.NaT, index=raw.index))),
        errors='coerce', dayfirst=True
    )
    raw['Clave_Referencia'] = raw.get('clave de referencia', raw.get('referencia', raw.get('asignacion', pd.Series('', index=raw.index)))).fillna('').astype(str).str.strip()
    raw['Fecha_Emision_OC'] = pd.to_datetime(raw.get('fecha emision oc'), errors='coerce', dayfirst=True)

    f_entrega = raw.get('fecha de entrega', raw.get('fecha entrega oc', raw.get('fecha de entrega oc', pd.Series(pd.NaT, index=raw.index))))
    raw['Fecha_Entrega_OC'] = pd.to_datetime(f_entrega, errors='coerce', format='mixed')
    raw['Fecha_Aprobacion_OC'] = pd.to_datetime(raw.get('fecha aprobacion final oc'), errors='coerce', dayfirst=True)
    raw['Primera_Fecha_Entrega_OC'] = pd.to_datetime(raw.get('primera fecha entrega oc'), errors='coerce', dayfirst=True)

    prov_series = raw.get('nombre', raw.get('proveedor', raw.get('proveedor/centro suministrador', pd.Series('', index=raw.index))))
    raw['Proveedor'] = prov_series.fillna('DESCONOCIDO').astype(str).str.strip()

    op_candidates = [
        'operador de oc', 'operador de co', 'operador oc', 'operador_oc',
        'operador_co', 'operador co', 'operador'
    ]
    col_operador_oc = None
    for cand in op_candidates:
        if cand in raw.columns:
            col_operador_oc = cand
            break

    if col_operador_oc is None and len(raw.columns) > 0:
        col_operador_oc = raw.columns[-1]

    if col_operador_oc is not None and col_operador_oc in raw.columns:
        raw['Operador_OC'] = raw[col_operador_oc].fillna(raw['Key'].map(op_map)).fillna('SIN ASIGNAR').astype(str).str.strip()
    else:
        raw['Operador_OC'] = raw['Key'].map(op_map).fillna('SIN ASIGNAR').astype(str).str.strip()

    raw['Operador_OC'] = raw['Operador_OC'].replace({'nan': 'SIN ASIGNAR', '': 'SIN ASIGNAR', 'None': 'SIN ASIGNAR'})
    mask_sin = raw['Operador_OC'] == 'SIN ASIGNAR'
    if mask_sin.any():
        fallback_map = raw.loc[mask_sin, 'Key'].map(op_map)
        raw.loc[mask_sin, 'Operador_OC'] = fallback_map.fillna('SIN ASIGNAR')

    raw['Operador_VA'] = raw.get('operador de va', raw.get('operador_va', pd.Series('SIN ASIGNAR', index=raw.index))).fillna('SIN ASIGNAR').astype(str).str.strip()
    raw['Division'] = raw.get('division', pd.Series('S/D', index=raw.index)).fillna('S/D').astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    gc_series = raw.get('grupo de compras', raw.get('grupo de compra oc', raw.get('grupo compras', pd.Series('SIN GRUPO', index=raw.index))))
    raw['Grupo_Compras'] = gc_series.fillna('SIN GRUPO').astype(str).str.strip()

    df_docs = raw

    today_date = pd.to_datetime(corte_str, dayfirst=True)
    if pd.isna(today_date):
        today_date = pd.Timestamp.now().normalize()

    def first_valid(series, default=''):
        for val in series:
            if pd.notna(val) and str(val).strip() not in ['', 'None', 'nan', 'DESCONOCIDO', 'SIN ASIGNAR', 'SIN GRUPO']:
                return str(val).strip()
        return default

    def join_divisions(series):
        divs = sorted(set(str(x).strip() for x in series if pd.notna(x) and str(x).strip() not in ['', 'S/D', 'nan']))
        return '/'.join(divs) if divs else 'S/D'

    grouped = df_docs.groupby(['Sociedad', 'Pedido', 'Posicion']).agg(
        Proveedor=('Proveedor', lambda s: first_valid(s, 'DESCONOCIDO')),
        Operador_OC=('Operador_OC', lambda s: first_valid(s, 'SIN ASIGNAR')),
        Operador_VA=('Operador_VA', lambda s: first_valid(s, 'SIN ASIGNAR')),
        Division=('Division', join_divisions),
        Grupo_Compras=('Grupo_Compras', lambda s: first_valid(s, 'SIN GRUPO')),
        Fe_Contabilizacion=('Fe_Contabilizacion', lambda s: s.dropna().max() if len(s.dropna()) > 0 else pd.NaT),
        Clave_Referencia=('Clave_Referencia', lambda s: first_valid(s, '')),
        Fecha_Emision_OC=('Fecha_Emision_OC', 'first'),
        Fecha_Entrega_OC=('Fecha_Entrega_OC', lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else pd.NaT),
        Fecha_Aprobacion_OC=('Fecha_Aprobacion_OC', 'first'),
        Cant_Docs=('Clase_Doc', 'count'),
        Total_Debe=('Importe', lambda s: s[s > 0].sum()),
        Total_Haber=('Importe', lambda s: s[s < 0].sum()),
        Saldo_Neto=('Importe', 'sum'),
        Clases_Doc=('Clase_Doc', lambda s: ', '.join(sorted(set(str(x) for x in s if x)))),
        Fecha_Min_Doc=('Fecha_Doc', 'min'),
        Fecha_Max_Doc=('Fecha_Doc', 'max')
    ).reset_index()

    grouped['Total_Debe'] = grouped['Total_Debe'].round(2)
    grouped['Total_Haber'] = grouped['Total_Haber'].round(2)
    grouped['Saldo_Neto'] = grouped['Saldo_Neto'].round(2)
    grouped['Key'] = grouped['Sociedad'] + '_' + grouped['Pedido'] + '_' + grouped['Posicion']

    def diag_emrf(r):
        saldo = r['Saldo_Neto']
        debe = r['Total_Debe']
        haber = r['Total_Haber']
        if abs(saldo) < 0.01:
            return 'COMPENSABLE (Saldo $0)'
        elif saldo < 0:
            if debe == 0:
                return 'FALTA FACTURA (Solo Recepción)'
            else:
                return 'FALTA FACTURA (Recepción parcial sin facturar)'
        else:
            if haber == 0:
                return 'FALTA RECEPCIÓN (Solo Factura)'
            else:
                return 'FALTA RECEPCIÓN (Factura mayor a Recepción)'

    def group_emrf(diag):
        if 'FALTA FACTURA' in diag:
            return 'TIENE RECEPCIÓN - FALTA FACTURA'
        elif 'FALTA RECEPCIÓN' in diag:
            return 'TIENE FACTURA - FALTA RECEPCIÓN'
        else:
            return 'COMPENSABLE (Saldo $0)'

    def venc_status(fec):
        if pd.isna(fec):
            return 'SIN FECHA OC'
        elif fec < today_date:
            return 'VENCIDA'
        else:
            return 'VIGENTE'

    def dias_atraso(fec):
        if pd.isna(fec):
            return 0
        delta = (today_date - fec).days
        return int(delta) if delta > 0 else 0

    def calc_prioridad(r):
        emrf = r['Grupo_EMRF']
        venc = r['Estado_Vencimiento']
        if emrf == 'TIENE FACTURA - FALTA RECEPCIÓN':
            if venc == 'VENCIDA':
                return '🔴 URGENTE: OC Vencida sin Recepción'
            else:
                return '🟠 Factura sin Recepción (En plazo)'
        elif emrf == 'TIENE RECEPCIÓN - FALTA FACTURA':
            if venc == 'VENCIDA':
                return '🟡 RECLAMAR: OC Vencida sin Factura'
            else:
                return '🔵 Recepción en plazo (Pendiente Factura)'
        else:
            return '🟢 Listo para compensar (F.13)'

    grouped['Diagnostico_EMRF'] = grouped.apply(diag_emrf, axis=1)
    grouped['Grupo_EMRF'] = grouped['Diagnostico_EMRF'].apply(group_emrf)
    grouped['Estado_Vencimiento'] = grouped['Fecha_Entrega_OC'].apply(venc_status)
    grouped['Dias_Atraso'] = grouped['Fecha_Entrega_OC'].apply(dias_atraso)
    grouped['Prioridad_Accion'] = grouped.apply(calc_prioridad, axis=1)

    def fmt_date(d):
        return d.strftime('%Y-%m-%d') if pd.notna(d) else None

    records = []
    for _, r in grouped.iterrows():
        records.append({
            'Sociedad': str(r['Sociedad']),
            'Pedido': str(r['Pedido']),
            'Posicion': str(r['Posicion']),
            'Proveedor': str(r['Proveedor']),
            'Grupo_Compras': str(r['Grupo_Compras']),
            'Operador_OC': str(r['Operador_OC']),
            'Operador_VA': str(r['Operador_VA']),
            'Division': str(r['Division']),
            'Fe_Contabilizacion': fmt_date(r['Fe_Contabilizacion']),
            'Fecha_Entrega_OC': fmt_date(r['Fecha_Entrega_OC']),
            'Fecha_Emision_OC': fmt_date(r['Fecha_Emision_OC']),
            'Dias_Atraso': int(r['Dias_Atraso']),
            'Total_Debe': float(r['Total_Debe']),
            'Total_Haber': float(r['Total_Haber']),
            'Saldo_Neto': float(r['Saldo_Neto']),
            'Estado_Vencimiento': str(r['Estado_Vencimiento']),
            'Grupo_EMRF': str(r['Grupo_EMRF']),
            'Diagnostico_EMRF': str(r['Diagnostico_EMRF']),
            'Prioridad_Accion': str(r['Prioridad_Accion']),
            'Cant_Docs': int(r['Cant_Docs']),
            'Clases_Doc': str(r['Clases_Doc']),
            'Clave_Referencia': str(r['Clave_Referencia'])
        })

    out_payload = {
        'metadata': {
            'fecha_corte': corte_str,
            'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_posiciones': len(records),
            'sociedades': sorted(list(set(r['Sociedad'] for r in records)))
        },
        'data': records
    }

    out_file = os.path.join(data_dir, 'partidas_emrf.json')
    with open(out_file, 'w', encoding='utf-8') as f_out:
        json.dump(out_payload, f_out, ensure_ascii=False, indent=None)

    print(f"Archivo generado exitosamente en {out_file}")
    print(f"Total posiciones: {len(records):,d}")
    return out_file

if __name__ == '__main__':
    arg_corte = sys.argv[1] if len(sys.argv) > 1 else None
    process_data(corte_str=arg_corte)
