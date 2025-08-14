import os
import shutil
import subprocess

# Carpetas de salida
for folder in ("build", "dist", "main.spec"):
    if os.path.exists(folder):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        else:
            os.remove(folder)

# Comando de PyInstaller
cmd = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "main.py"
]

# Ejecutar build

subprocess.run(" ".join(cmd), shell=True, check=True)
