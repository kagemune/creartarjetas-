import PyInstaller.__main__
import os

# Crear el ejecutable
PyInstaller.__main__.run([
    'main.py',
    '--name=GeneradorDeTarjetas',
    '--onefile',
    '--windowed',
    '--add-data=tarjetasEmpleados.html;.',
    '--hidden-import=win32com',  # ← Añade esta línea
    '--hidden-import=win32api',  # ← Y esta
    # '--icon=assets/icono.ico',
    '--clean'
])