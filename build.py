import PyInstaller.__main__
import os

# Obtener la ruta actual
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',
    '--name=GeneradorDeTarjetas',
    '--onefile',
    '--windowed',
    '--add-data=templates;templates',
    '--add-data=assets;assets',
    '--add-data=tarjetasEmpleados1.html;.',
    '--icon=assets/icono.ico',
    '--clean',
    '--noconfirm'
])