# -*- coding: utf-8 -*-
"""
generar_partidas_abiertas.py
----------------------------
Genera el archivo final consolidado 'Partidas abiertas.xlsx' (y .csv) a partir de los
archivos base de SAP:
  - FBL3N.xlsx : Base contable de partidas de la cuenta EM/RF (incluye columna 'Sociedad')
  - ME2L.xlsx  : Reporte de compras (aporta Fecha de entrega, Grupo de compras, Proveedor)
  - Z909.xlsx  : Maestro de compras (aporta OPERADOR OC)

Lógica de cruce:
  1. En FBL3N se concatena: Documento compras + Posición -> CONCATENA
  2. Con ME2L se cruza por CONCATENA para completar:
       - Fecha de entrega
       - Grupo de compras
       - Proveedor/Centro suministrador
  3. Con Z909 se cruza por CONCATENA para completar:
       - OPERADOR OC (con fallback a operadores_map.json si está disponible)
  4. El archivo final resultante mantiene exactamente las columnas estándar y el formato.
"""

import os
import sys
import json
import shutil
import datetime
import numpy as np
import pandas as pd

def clean_key(doc, pos):
    """Convierte doc y pos a string numérico limpio para la concatenación."""
    if pd.isna(doc) or pd.isna(pos):
        return None
    try:
        d = str(int(round(float(doc))))
        p = str(int(round(float(pos))))
        return d + p
    except Exception:
        return None

def find_source_files(custom_dirs=None):
    """
    Busca los archivos base FBL3N.xlsx, ME2L.xlsx y Z909.xlsx en los directorios candidatos.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_data_dir = os.path.join(os.path.dirname(script_dir), "data")
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop", "PARTIDAS ABIERTAS")

    candidates = []
    if custom_dirs:
        if isinstance(custom_dirs, str):
            custom_dirs = [custom_dirs]
        candidates.extend(custom_dirs)
    candidates.extend([repo_data_dir, desktop_dir])

    files_found = {'FBL3N': None, 'ME2L': None, 'Z909': None}

    # Revisar candidatos priorizando el archivo más reciente si existe en varios lugares
    for name in ['FBL3N', 'ME2L', 'Z909']:
        newest_path = None
        newest_mtime = -1
        for d in candidates:
            if not os.path.exists(d):
                continue
            for ext in ['.xlsx', '.XLSX', '.xls', '.XLS']:
                fpath = os.path.join(d, f"{name}{ext}")
                if os.path.exists(fpath):
                    mtime = os.path.getmtime(fpath)
                    if mtime > newest_mtime:
                        newest_mtime = mtime
                        newest_path = fpath
        files_found[name] = newest_path

    return files_found, repo_data_dir, desktop_dir

def sync_base_files_to_data(files_found, repo_data_dir):
    """Copia los archivos base a data/ del repositorio si vinieron de otra carpeta."""
    if not os.path.exists(repo_data_dir):
        os.makedirs(repo_data_dir, exist_ok=True)

    for name, fpath in files_found.items():
        if fpath and os.path.exists(fpath):
            target = os.path.join(repo_data_dir, f"{name}.xlsx")
            # Si no está en repo_data_dir o el origen es más reciente
            try:
                if not os.path.exists(target) or os.path.getmtime(fpath) > os.path.getmtime(target):
                    shutil.copy2(fpath, target)
                    print(f"[SYNC] Copiado {os.path.basename(fpath)} -> {target}")
            except Exception as e:
                print(f"[WARN] No se pudo sincronizar {name} a data: {e}")

def build_partidas_abiertas(custom_dir=None, verbose=True):
    """
    Construye el DataFrame y genera 'Partidas abiertas.xlsx' y 'Partidas abiertas.csv'.
    """
    files_found, repo_data_dir, desktop_dir = find_source_files(custom_dir)

    missing = [k for k, v in files_found.items() if not v or not os.path.exists(v)]
    if missing:
        raise FileNotFoundError(f"No se encontraron los siguientes archivos base: {', '.join(missing)}")

    if verbose:
        print("=== GENERACIÓN DE PARTIDAS ABIERTAS ===")
        print(f"FBL3N : {files_found['FBL3N']}")
        print(f"ME2L  : {files_found['ME2L']}")
        print(f"Z909  : {files_found['Z909']}")

    # 1. Cargar FBL3N
    sheet_fbl3n = 'Data'
    try:
        df_fbl3n = pd.read_excel(files_found['FBL3N'], sheet_name=sheet_fbl3n)
    except Exception:
        df_fbl3n = pd.read_excel(files_found['FBL3N'])

    # Limpiar filas totalmente vacías o sin documento de compras
    df_fbl3n = df_fbl3n.dropna(how='all').copy()
    if 'Documento compras' in df_fbl3n.columns:
        df_fbl3n = df_fbl3n.dropna(subset=['Documento compras']).copy()
    if 'Posición' in df_fbl3n.columns:
        df_fbl3n = df_fbl3n.dropna(subset=['Posición']).copy()

    # 2. Cargar ME2L
    try:
        df_me2l = pd.read_excel(files_found['ME2L'], sheet_name='Data')
    except Exception:
        df_me2l = pd.read_excel(files_found['ME2L'])

    # 3. Cargar Z909
    try:
        df_z909 = pd.read_excel(files_found['Z909'], sheet_name='Data')
    except Exception:
        df_z909 = pd.read_excel(files_found['Z909'])

    # 4. Generar columna CONCATENA
    df_fbl3n['CONCATENA'] = [clean_key(d, p) for d, p in zip(df_fbl3n['Documento compras'], df_fbl3n['Posición'])]
    
    # En ME2L: 'Documento compras' y 'Posición'
    me2l_doc_col = next((c for c in df_me2l.columns if 'documento' in str(c).lower() and 'compras' in str(c).lower()), 'Documento compras')
    me2l_pos_col = next((c for c in df_me2l.columns if 'posici' in str(c).lower()), 'Posición')
    df_me2l['CONCATENA'] = [clean_key(d, p) for d, p in zip(df_me2l[me2l_doc_col], df_me2l[me2l_pos_col])]

    # En Z909: 'NRO. OC' y 'POS. OC'
    z909_doc_col = next((c for c in df_z909.columns if 'nro' in str(c).lower() or 'documento' in str(c).lower() or 'pedido' in str(c).lower()), 'NRO. OC')
    z909_pos_col = next((c for c in df_z909.columns if 'pos' in str(c).lower()), 'POS. OC')
    df_z909['CONCATENA'] = [clean_key(d, p) for d, p in zip(df_z909[z909_doc_col], df_z909[z909_pos_col])]

    # Deduplicar tablas de consulta por CONCATENA
    df_me2l_clean = df_me2l.dropna(subset=['CONCATENA']).drop_duplicates(subset=['CONCATENA']).copy()
    df_z909_clean = df_z909.dropna(subset=['CONCATENA']).drop_duplicates(subset=['CONCATENA']).copy()

    # Columnas de ME2L a cruzar: Fecha de entrega, Grupo de compras, Proveedor/Centro suministrador
    me2l_entrega_col = next((c for c in df_me2l_clean.columns if 'entrega' in str(c).lower()), 'Fecha de entrega')
    me2l_grupo_col = next((c for c in df_me2l_clean.columns if 'grupo' in str(c).lower()), 'Grupo de compras')
    me2l_prov_col = next((c for c in df_me2l_clean.columns if 'proveedor' in str(c).lower()), 'Proveedor/Centro suministrador')

    me2l_sub = df_me2l_clean[['CONCATENA', me2l_entrega_col, me2l_grupo_col, me2l_prov_col]].copy()
    me2l_sub.columns = ['CONCATENA', 'Fecha de entrega', 'Grupo de compras', 'Proveedor/Centro suministrador']

    # Columnas de Z909 a cruzar: OPERADOR OC
    z909_op_col = next((c for c in df_z909_clean.columns if 'operador' in str(c).lower()), 'OPERADOR OC')
    z909_sub = df_z909_clean[['CONCATENA', z909_op_col]].copy()
    z909_sub.columns = ['CONCATENA', 'OPERADOR OC']

    # 5. Realizar el merge (cruce tipo BUSCARV / LEFT JOIN)
    merged = df_fbl3n.merge(me2l_sub, on='CONCATENA', how='left')
    merged = merged.merge(z909_sub, on='CONCATENA', how='left')

    # Fallback con operadores_map.json si está disponible y hay vacíos
    op_map = {}
    for map_dir in [repo_data_dir, desktop_dir]:
        op_path = os.path.join(map_dir, 'operadores_map.json')
        if os.path.exists(op_path):
            try:
                with open(op_path, 'r', encoding='utf-8') as f_op:
                    op_map.update(json.load(f_op))
            except Exception:
                pass

    if op_map and 'Sociedad' in merged.columns:
        def get_op_fallback(row):
            current = row.get('OPERADOR OC')
            if pd.notna(current) and str(current).strip() not in ['', 'None', 'nan', 'SIN ASIGNAR']:
                return str(current).strip()
            # Formato clave: SOCIEDAD_PEDIDO_POSICION
            try:
                soc = str(row.get('Sociedad', '')).strip()
                ped = str(int(round(float(row.get('Documento compras', 0)))))
                pos = str(int(round(float(row.get('Posición', 0)))))
                k = f"{soc}_{ped}_{pos}"
                return op_map.get(k, current)
            except Exception:
                return current

        merged['OPERADOR OC'] = merged.apply(get_op_fallback, axis=1)

    # Asegurar que códigos y números largos (Documento compras, Posición, CONCATENA) sean texto limpio sin puntos ni notación científica
    def to_clean_str_code(v):
        if pd.isna(v) or v is None:
            return ""
        try:
            return str(int(round(float(v))))
        except Exception:
            return str(v).strip()

    if 'Documento compras' in merged.columns:
        merged['Documento compras'] = merged['Documento compras'].apply(to_clean_str_code)
    if 'Posición' in merged.columns:
        merged['Posición'] = merged['Posición'].apply(to_clean_str_code)
    if 'CONCATENA' in merged.columns:
        merged['CONCATENA'] = merged['CONCATENA'].apply(to_clean_str_code)
    if 'Nº documento' in merged.columns:
        merged['Nº documento'] = merged['Nº documento'].apply(to_clean_str_code)

    # Orden exacto de columnas para garantizar consistencia total
    desired_cols = [
        'Sociedad',
        'Icono part.abiertas/comp.',
        'Asignación',
        'Nº documento',
        'División',
        'Clase de documento',
        'Fecha de documento',
        'Clave contabiliz.',
        'Importe en moneda local',
        'Moneda local',
        'Indicador impuestos',
        'Doc.compensación',
        'Nombre',
        'Fe.contabilización',
        'Documento compras',
        'Posición',
        'CONCATENA',
        'Fecha de entrega',
        'Grupo de compras',
        'Proveedor/Centro suministrador',
        'OPERADOR OC'
    ]

    # Reordenar columnas manteniendo cualquier columna adicional que pudiera venir
    final_cols = [c for c in desired_cols if c in merged.columns]
    remaining_cols = [c for c in merged.columns if c not in final_cols]
    final_df = merged[final_cols + remaining_cols].copy()

    # 6. Guardar en los destinos
    target_dirs = [repo_data_dir, desktop_dir]
    for out_d in target_dirs:
        if not os.path.exists(out_d):
            continue
        xlsx_file = os.path.join(out_d, "Partidas abiertas.xlsx")
        csv_file = os.path.join(out_d, "Partidas abiertas.csv")
        
        try:
            # Guardar Excel con hoja 'Data'
            with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
                final_df.to_excel(writer, sheet_name='Data', index=False)
            if verbose:
                print(f"[OK] Guardado Excel en: {xlsx_file} ({len(final_df):,d} filas)")
        except Exception as e:
            print(f"[ERROR] Error al guardar {xlsx_file}: {e}")

        try:
            # Guardar CSV UTF-8 para lectura ultrarrápida
            final_df.to_csv(csv_file, index=False, encoding='utf-8')
            if verbose:
                print(f"[OK] Guardado CSV en: {csv_file}")
        except Exception as e:
            print(f"[ERROR] Error al guardar {csv_file}: {e}")

    # Sincronizar bases a repo_data_dir
    sync_base_files_to_data(files_found, repo_data_dir)

    return final_df

if __name__ == '__main__':
    custom = sys.argv[1] if len(sys.argv) > 1 else None
    build_partidas_abiertas(custom_dir=custom, verbose=True)
