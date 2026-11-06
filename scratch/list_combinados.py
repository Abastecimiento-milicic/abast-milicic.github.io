import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

combinados_dir = "data/Almacen MB52/Combinados"
if os.path.exists(combinados_dir):
    print("Files in", combinados_dir)
    for f in os.listdir(combinados_dir):
        print(" ", f)
else:
    print("Directory does not exist:", combinados_dir)
