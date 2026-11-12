import csv
from collections import defaultdict

path = 'data - almacen/ALMACEN.csv'
with open(path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    month_counts = defaultdict(lambda: {
        'total_rows': 0,
        'has_fecha_ee': 0,
        'comp_sum': 0,
        'cumpl_at': 0,
        'cumpl_ft': 0,
        'no_cumpl': 0,
        'base_ros_1': 0,
        'base_sj_1': 0,
        'no_base': 0
    })
    
    for r in reader:
        fee = r.get('FECHA ENTREGA ESPERADA', '').strip()
        ym = 'NO_FECHA'
        if fee:
            parts = fee.replace('/', '-').split('-')
            if len(parts) == 3:
                if len(parts[2]) == 4:
                    ym = f"{parts[2]}-{parts[1].zfill(2)}"
                elif len(parts[0]) == 4:
                    ym = f"{parts[0]}-{parts[1].zfill(2)}"
        
        st = month_counts[ym]
        st['total_rows'] += 1
        if fee: st['has_fecha_ee'] += 1
        
        def to_num(v):
            try:
                return float(str(v).replace(',', '.').strip())
            except:
                return 0.0
                
        st['comp_sum'] += to_num(r.get('COMPROMETIDOS', 0))
        st['cumpl_at'] += to_num(r.get('CUMPLIDO AT', 0))
        st['cumpl_ft'] += to_num(r.get('CUMPLIDO FT', 0))
        st['no_cumpl'] += to_num(r.get('NO CUMPLIDO ALMACEN', 0))
        
        bros = r.get('BASE ROS', '').strip()
        bsj = r.get('BASE SJ', '').strip()
        if bros == '1':
            st['base_ros_1'] += 1
        elif bsj == '1':
            st['base_sj_1'] += 1
        else:
            st['no_base'] += 1

print('MONTH BREAKDOWN IN ALMACEN.csv:')
for ym in sorted(month_counts.keys()):
    if ym.startswith('2025') or ym.startswith('2026') or ym == 'NO_FECHA':
        d = month_counts[ym]
        print(f"{ym}: total_rows={d['total_rows']}, comp_sum={int(d['comp_sum'])}, AT={int(d['cumpl_at'])}, FT={int(d['cumpl_ft'])}, NO={int(d['no_cumpl'])}, ROS={d['base_ros_1']}, SJ={d['base_sj_1']}, SinBase={d['no_base']}")
