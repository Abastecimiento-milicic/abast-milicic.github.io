import os
import sys
import re
import json
import unicodedata
import datetime
import numpy as np
import pandas as pd

def clean_col(c):
    nfkd = unicodedata.normalize('NFKD', str(c))
    return ''.join([ch for ch in nfkd if not unicodedata.combining(ch)]).lower().strip()

def clean_num(s):
    return pd.to_numeric(s, errors='coerce').fillna(-1).astype(np.int64).astype(str)

def get_default_corte():
    try:
        last_update_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "js", "last-update.js")
        if os.path.exists(last_update_path):
            with open(last_update_path, "r", encoding="utf-8") as f:
                m = re.search(r'LAST_UPDATE\s*=\s*["\']([^"\']+)["\']', f.read())
                if m:
                    return m.group(1).strip()
    except Exception:
        pass
    return datetime.datetime.now().strftime("%d/%m/%Y")

def find_data_file(base_dirs, file_prefix):
    """Busca un archivo por prefijo (FBL3N, ME2L, Z909) con extensiones .xlsx, .xls o .csv."""
    extensions = ['.xlsx', '.XLSX', '.xls', '.XLS', '.csv', '.CSV']
    for bdir in base_dirs:
        if not os.path.isdir(bdir):
            continue
        for ext in extensions:
            candidate = os.path.join(bdir, f"{file_prefix}{ext}")
            if os.path.exists(candidate):
                return candidate
        # Búsqueda case-insensitive flexible
        for fname in os.listdir(bdir):
            if fname.lower().startswith(file_prefix.lower()) and any(fname.lower().endswith(e.lower()) for e in extensions):
                return os.path.join(bdir, fname)
    return None

def read_tabular_file(fpath):
    """Lee un archivo Excel o CSV retornando un DataFrame de pandas."""
    if fpath.lower().endswith('.csv'):
        # Probar separador punto y coma y luego coma
        try:
            return pd.read_csv(fpath, sep=';', encoding='utf-8', low_memory=False)
        except Exception:
            return pd.read_csv(fpath, sep=',', encoding='latin-1', low_memory=False)
    else:
        # Excel: si tiene hoja 'Data' usarla, sino la primera hoja
        try:
            return pd.read_excel(fpath, sheet_name='Data')
        except Exception:
            return pd.read_excel(fpath, sheet_name=0)

def process_data(data_dir=None, corte_str=None):
    if corte_str is None:
        corte_str = get_default_corte()
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

    candidate_dirs = [
        os.path.join(data_dir, 'data PARTIDAS ABIERTAS'),
        data_dir
    ]

    fbl3n_path = find_data_file(candidate_dirs, 'FBL3N')
    me2l_path = find_data_file(candidate_dirs, 'ME2L')
    z909_path = find_data_file(candidate_dirs, 'Z909')

    if not fbl3n_path:
        print("[ERROR] No se encontro el archivo FBL3N (.xlsx / .csv) en data PARTIDAS ABIERTAS ni en data.")
        return None

    print("=" * 75)
    print("      PROCESAMIENTO DE PARTIDAS ABIERTAS EM/RF (FBL3N + ME2L + Z909)")
    print("=" * 75)
    print(f"FBL3N : {fbl3n_path}")
    print(f"ME2L  : {me2l_path or 'No disponible'}")
    print(f"Z909  : {z909_path or 'No disponible'}")
    print("-" * 75)

    # 1. Cargar FBL3N (Base transaccional principal)
    print("Cargando FBL3N...")
    raw_fbl3n = read_tabular_file(fbl3n_path)
    raw_fbl3n.rename(columns={c: clean_col(c) for c in raw_fbl3n.columns}, inplace=True)

    # Validar columnas mínimas
    key_cols = [k for k in ['documento compras', 'posicion', 'clave contabiliz.'] if k in raw_fbl3n.columns]
    if len(key_cols) < 3:
        print(f"[ERROR] FBL3N no contiene las columnas necesarias (documento compras, posicion, clave contabiliz.). Columnas: {list(raw_fbl3n.columns)}")
        return None

    df_f = raw_fbl3n.dropna(subset=key_cols).copy()
    df_f['Pedido'] = clean_num(df_f['documento compras'])
    df_f['Posicion'] = clean_num(df_f['posicion'])

    # Si existe columna 'sociedad' en FBL3N, usarla; si no, marcar S/D
    if 'sociedad' in df_f.columns:
        df_f['Sociedad'] = df_f['sociedad'].fillna('S/D').astype(str).str.strip()
    else:
        df_f['Sociedad'] = 'S/D'

    df_f['Key'] = df_f['Sociedad'] + '_' + df_f['Pedido'] + '_' + df_f['Posicion']
    df_f['Join_Key'] = df_f['Pedido'] + '_' + df_f['Posicion']

    print(f"-> FBL3N procesado: {len(df_f):,d} partidas validas.")

    # 2. Cargar ME2L (Fechas de entrega, Grupos de compra y Proveedor OC)
    me2l_fentrega = {}
    me2l_gc = {}
    me2l_prov = {}

    if me2l_path:
        print("Cargando ME2L...")
        df_m = read_tabular_file(me2l_path)
        df_m.rename(columns={c: clean_col(c) for c in df_m.columns}, inplace=True)

        col_doc_m = next((c for c in ['documento compras', 'nro. oc', 'nro oc', 'pedido'] if c in df_m.columns), None)
        col_pos_m = next((c for c in ['posicion', 'pos. oc', 'pos oc', 'pos'] if c in df_m.columns), None)

        if col_doc_m and col_pos_m:
            df_m['Pedido'] = clean_num(df_m[col_doc_m])
            df_m['Posicion'] = clean_num(df_m[col_pos_m])
            df_m['Join_Key'] = df_m['Pedido'] + '_' + df_m['Posicion']
            df_m = df_m.drop_duplicates(subset=['Join_Key']).copy()

            if 'fecha de entrega' in df_m.columns:
                me2l_fentrega = dict(zip(df_m['Join_Key'], pd.to_datetime(df_m['fecha de entrega'], errors='coerce', dayfirst=True)))
            if 'grupo de compras' in df_m.columns:
                me2l_gc = dict(zip(df_m['Join_Key'], df_m['grupo de compras'].fillna('SIN GRUPO').astype(str).str.strip()))
            
            col_prov_m = next((c for c in ['proveedor/centro suministrador', 'proveedor', 'nombre'] if c in df_m.columns), None)
            if col_prov_m:
                me2l_prov = dict(zip(df_m['Join_Key'], df_m[col_prov_m].fillna('').astype(str).str.strip()))

            print(f"-> ME2L procesado: {len(df_m):,d} pedidos/posiciones indexados.")

    # 3. Cargar Z909 (Operador OC)
    z909_op = {}
    if z909_path:
        print("Cargando Z909...")
        df_z = read_tabular_file(z909_path)
        df_z.rename(columns={c: clean_col(c) for c in df_z.columns}, inplace=True)

        col_doc_z = next((c for c in ['nro. oc', 'nro oc', 'documento compras', 'pedido'] if c in df_z.columns), None)
        col_pos_z = next((c for c in ['pos. oc', 'pos oc', 'posicion'] if c in df_z.columns), None)
        col_op_z = next((c for c in ['operador oc', 'operador_oc', 'operador de oc', 'operador'] if c in df_z.columns), None)

        if col_doc_z and col_pos_z and col_op_z:
            df_z['Pedido'] = clean_num(df_z[col_doc_z])
            df_z['Posicion'] = clean_num(df_z[col_pos_z])
            df_z['Join_Key'] = df_z['Pedido'] + '_' + df_z['Posicion']
            df_z_valid = df_z[df_z[col_op_z].notna() & (df_z[col_op_z].astype(str).str.strip() != '')].drop_duplicates(subset=['Join_Key'])
            z909_op = dict(zip(df_z_valid['Join_Key'], df_z_valid[col_op_z].astype(str).str.strip()))
            print(f"-> Z909 procesado: {len(z909_op):,d} operadores OC indexados.")

    # 4. Cargar mapa auxiliar de operadores si existe
    op_map = {}
    map_path = os.path.join(data_dir, 'operadores_map.json')
    if os.path.exists(map_path):
        try:
            with open(map_path, 'r', encoding='utf-8') as f_op:
                op_map = json.load(f_op)
        except Exception as e:
            print(f"Error al cargar operadores_map.json: {e}")

    # 5. Enriquecer DataFrame FBL3N con datos de ME2L, Z909 y auxiliares
    df_f['Fecha_Entrega_OC'] = df_f['Join_Key'].map(me2l_fentrega)
    df_f['Grupo_Compras'] = df_f['Join_Key'].map(me2l_gc).fillna('SIN GRUPO').replace({'nan': 'SIN GRUPO', '': 'SIN GRUPO', 'None': 'SIN GRUPO'})

    # Operador OC: Z909 -> op_map -> 'SIN ASIGNAR'
    df_f['Operador_OC'] = df_f['Join_Key'].map(z909_op).fillna(df_f['Key'].map(op_map)).fillna('SIN ASIGNAR')
    df_f['Operador_OC'] = df_f['Operador_OC'].replace({'nan': 'SIN ASIGNAR', '': 'SIN ASIGNAR', 'None': 'SIN ASIGNAR'})
    mask_sin = df_f['Operador_OC'] == 'SIN ASIGNAR'
    if mask_sin.any():
        fallback_map = df_f.loc[mask_sin, 'Key'].map(op_map)
        df_f.loc[mask_sin, 'Operador_OC'] = fallback_map.fillna('SIN ASIGNAR')

    df_f['Operador_VA'] = 'SIN ASIGNAR'

    # Proveedor: Nombre en FBL3N -> ME2L Proveedor -> 'DESCONOCIDO'
    prov_raw = df_f.get('nombre', pd.Series('', index=df_f.index)).fillna('').astype(str).str.strip()
    prov_fallback = df_f['Join_Key'].map(me2l_prov).fillna('').apply(lambda x: re.sub(r'^\d+\s*', '', str(x)).strip())
    df_f['Proveedor'] = np.where((prov_raw != '') & (prov_raw.str.lower() != 'nan'), prov_raw, prov_fallback)
    df_f['Proveedor'] = df_f['Proveedor'].replace({'': 'DESCONOCIDO', 'nan': 'DESCONOCIDO', 'None': 'DESCONOCIDO'})

    df_f['Division'] = df_f.get('division', pd.Series('S/D', index=df_f.index)).fillna('S/D').astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_f['Importe'] = pd.to_numeric(df_f.get('importe en moneda local'), errors='coerce').fillna(0.0)
    df_f['Moneda'] = df_f.get('moneda local', pd.Series('ARS', index=df_f.index)).fillna('ARS')

    df_f['Clave_Contab'] = df_f['clave contabiliz.'].astype(int).astype(str)
    df_f['Clase_Doc'] = df_f.get('clase de documento', pd.Series('', index=df_f.index)).fillna('').astype(str).str.strip()
    df_f['Doc_SAP'] = df_f.get('no documento', pd.Series('', index=df_f.index)).fillna(0).astype(np.int64).astype(str)

    df_f['Fecha_Doc'] = pd.to_datetime(df_f.get('fecha de documento'), errors='coerce', dayfirst=True)
    df_f['Fe_Contabilizacion'] = pd.to_datetime(
        df_f.get('fe.contabilizacion', df_f.get('fecha de contabilizacion', pd.Series(pd.NaT, index=df_f.index))),
        errors='coerce', dayfirst=True
    )
    df_f['Clave_Referencia'] = df_f.get('clave de referencia', df_f.get('referencia', df_f.get('asignacion', pd.Series('', index=df_f.index)))).fillna('').astype(str).str.strip()
    df_f['Fecha_Emision_OC'] = pd.NaT

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

    print("Agrupando posiciones por Sociedad, Pedido y Posicion...")
    grouped = df_f.groupby(['Sociedad', 'Pedido', 'Posicion']).agg(
        Proveedor=('Proveedor', lambda s: first_valid(s, 'DESCONOCIDO')),
        Operador_OC=('Operador_OC', lambda s: first_valid(s, 'SIN ASIGNAR')),
        Operador_VA=('Operador_VA', lambda s: first_valid(s, 'SIN ASIGNAR')),
        Division=('Division', join_divisions),
        Grupo_Compras=('Grupo_Compras', lambda s: first_valid(s, 'SIN GRUPO')),
        Fe_Contabilizacion=('Fe_Contabilizacion', lambda s: s.dropna().max() if len(s.dropna()) > 0 else pd.NaT),
        Clave_Referencia=('Clave_Referencia', lambda s: first_valid(s, '')),
        Fecha_Emision_OC=('Fecha_Emision_OC', 'first'),
        Fecha_Entrega_OC=('Fecha_Entrega_OC', lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else pd.NaT),
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

    # Guardar en data PARTIDAS ABIERTAS y en data como respaldo
    target_paths = [
        os.path.join(data_dir, 'data PARTIDAS ABIERTAS', 'partidas_emrf.json'),
        os.path.join(data_dir, 'partidas_emrf.json')
    ]

    for out_file in target_paths:
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, 'w', encoding='utf-8') as f_out:
            json.dump(out_payload, f_out, ensure_ascii=False, indent=None)
        print(f"Archivo guardado exitosamente: {out_file}")

    print(f"Total posiciones calculadas: {len(records):,d}")
    print(f"Sociedades incluidas: {', '.join(out_payload['metadata']['sociedades'])}")
    return target_paths[0]

if __name__ == '__main__':
    arg_corte = sys.argv[1] if len(sys.argv) > 1 else None
    process_data(corte_str=arg_corte)
