import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/combinar_mb52_analisis_mm.py', 'r', encoding='utf-8') as f:
    code = f.read()

def norm(t): return t.replace('\r\n', '\n')
code_norm = norm(code)

old_target = norm('''            elif 'stock' in c_lower and 'esp' in c_lower:
                col_rename[col] = 'Stock especial'
            elif 'unidad' in c_lower and 'med' in c_lower:
                col_rename[col] = 'Unidad medida base'
        if col_rename:
            df_mb.rename(columns=col_rename, inplace=True)

        if 'Material' not in df_mb.columns:
            print(f"  [SKIP] No tiene columna 'Material'. Omitiendo.")
            continue

        # Eliminar filas vacías o fila de total resumen
        df_clean = df_mb.dropna(subset=['Material']).copy()
        if df_clean.empty:
            print(f"  [SKIP] Archivo vacío después de filtrar materiales.")
            continue

        # Enriquecer cada fila
        enriched_rows = []
        for _, r in df_clean.iterrows():
            mat_raw = r['Material']
            mat_clean = norm_mat(mat_raw)
            alm_raw = r.get('Almacén', '')
            alm_candidates = alm_keys(alm_raw)

            row_mm = None
            for a in alm_candidates:
                if (a, mat_clean) in mm_exact:
                    row_mm = mm_exact[(a, mat_clean)]
                    break

            tipo_mat = ''
            if row_mm is not None:
                caract = str(row_mm.get('Caract.planif.nec.', '') or '').strip() or 'PLANIFICADO'
                if caract.upper() == 'NO PLANIFICADO':
                    caract = '-'
                planif = 'SI'
                estado_mm = str(row_mm.get('Estado', '') or '').strip() or 'PLANIFICADO'
                pp = row_mm.get('Punto de pedido', 0)
                stk_max = row_mm.get('Stock alm.máx.', 0)
                rubro = str(row_mm.get('Rubro', '') or '').strip()
                subrubro = str(row_mm.get('SubRubro', '') or '').strip()
                grp_comp = str(row_mm.get('Grupo de compras', '') or '').strip()
                tipo_mat = str(row_mm.get('Tipo material', '') or '').strip()
            else:
                caract = '-'
                planif = 'NO'
                estado_mm = 'NO PLANIFICADO'
                pp = 0
                stk_max = 0
                meta = mm_mat_meta.get(mat_clean, {})
                rubro = meta.get('Rubro', '')
                subrubro = meta.get('SubRubro', '')
                grp_comp = meta.get('Grupo de compras', '')
                tipo_mat = meta.get('Tipo material', '')''')

new_replacement = norm('''            elif 'stock' in c_lower and 'esp' in c_lower:
                col_rename[col] = 'Stock especial'
            elif 'unidad' in c_lower and 'med' in c_lower:
                col_rename[col] = 'Unidad medida base'
            elif 'tipo' in c_lower and 'mat' in c_lower:
                col_rename[col] = 'Tipo material'
        if col_rename:
            df_mb.rename(columns=col_rename, inplace=True)

        if 'Material' not in df_mb.columns:
            print(f"  [SKIP] No tiene columna 'Material'. Omitiendo.")
            continue

        # Eliminar filas vacías o fila de total resumen
        df_clean = df_mb.dropna(subset=['Material']).copy()
        if df_clean.empty:
            print(f"  [SKIP] Archivo vacío después de filtrar materiales.")
            continue

        # Enriquecer cada fila
        enriched_rows = []
        for _, r in df_clean.iterrows():
            mat_raw = r['Material']
            mat_clean = norm_mat(mat_raw)
            alm_raw = r.get('Almacén', '')
            alm_candidates = alm_keys(alm_raw)

            row_mm = None
            for a in alm_candidates:
                if (a, mat_clean) in mm_exact:
                    row_mm = mm_exact[(a, mat_clean)]
                    break

            # Prioridad 1: Obtener Tipo material directamente de Base MB52 si viene en el archivo
            tipo_mat = ''
            for c_tipo in ['Tipo material', 'Tipo de material', 'Tipo Material', 'MTART']:
                if c_tipo in r and pd.notna(r[c_tipo]):
                    v_tm = str(r[c_tipo]).strip()
                    if v_tm and v_tm.lower() not in ('nan', 'none', '-', ''):
                        tipo_mat = v_tm
                        break

            if row_mm is not None:
                caract = str(row_mm.get('Caract.planif.nec.', '') or '').strip() or 'PLANIFICADO'
                if caract.upper() == 'NO PLANIFICADO':
                    caract = '-'
                planif = 'SI'
                estado_mm = str(row_mm.get('Estado', '') or '').strip() or 'PLANIFICADO'
                pp = row_mm.get('Punto de pedido', 0)
                stk_max = row_mm.get('Stock alm.máx.', 0)
                rubro = str(row_mm.get('Rubro', '') or '').strip()
                subrubro = str(row_mm.get('SubRubro', '') or '').strip()
                grp_comp = str(row_mm.get('Grupo de compras', '') or '').strip()
                if not tipo_mat:
                    tipo_mat = str(row_mm.get('Tipo material', '') or '').strip()
            else:
                caract = '-'
                planif = 'NO'
                estado_mm = 'NO PLANIFICADO'
                pp = 0
                stk_max = 0
                meta = mm_mat_meta.get(mat_clean, {})
                rubro = meta.get('Rubro', '')
                subrubro = meta.get('SubRubro', '')
                grp_comp = meta.get('Grupo de compras', '')
                if not tipo_mat:
                    tipo_mat = meta.get('Tipo material', '')''')

if old_target in code_norm:
    code_norm = code_norm.replace(old_target, new_replacement, 1)
    with open('scripts/combinar_mb52_analisis_mm.py', 'w', encoding='utf-8') as f:
        f.write(code_norm)
    print("scripts/combinar_mb52_analisis_mm.py updated successfully!")
else:
    print("FAILED to find old_target in scripts/combinar_mb52_analisis_mm.py")
