import pandas as pd
from jinja2 import Environment, FileSystemLoader
from html2image import Html2Image
from PIL import Image
import time
# from weasyprint import HTML
import os
# 1. Crear rutas absolutas y normalizadas
base_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta del script
temp_dir = os.path.normpath(os.path.join(base_dir, "html2image_temp"))
output_dir = os.path.normpath(os.path.join(base_dir, "output_empleados"))

# 2. Crear directorios con permisos adecuados
os.makedirs(temp_dir, exist_ok=True, mode=0o777)
os.makedirs(output_dir, exist_ok=True, mode=0o777)

# def html_to_image_weasyprint(html_content, output_path):
#     HTML(string=html_content).write_png(output_path)
# 3. Configurar Html2Image con parámetros seguros
hti = Html2Image(
    temp_path=temp_dir,
    output_path=output_dir,
    size=(328, 208),
    custom_flags=[
        '--hide-scrollbars',
        '--default-background-color=00000000',  # Fondo transparente
        # '--window-size=328,208',                # Ajusta a tus necesidades
        '--force-device-scale-factor=1',
        '--disable-extensions',
        '--disable-popup-blocking',
        '--disable-infobars',
        '--disable-notifications',
        '--disable-gpu',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage'
     ]
)
# Configuración
csv_path = 'Asistencia y Novedades V3 - Personal.csv'
template_path = 'tarjetasEmpleados1.html'
output_folder = './tarjetas/'
os.makedirs(output_folder, exist_ok=True)

# def verificar_permisos(ruta):
#     try:
#         test_file = os.path.join(ruta, 'test.txt')
#         with open(test_file, 'w') as f:
#             f.write('test')
#         os.remove(test_file)
#         return True
#     except:
#         return False

# if not verificar_permisos(temp_dir):
#     temp_dir = os.path.normpath("C:/temp/html2image")
#     os.makedirs(temp_dir, exist_ok=True, mode=0o777)

# Cargar datos
df = pd.read_csv(csv_path)
# Verificar que el archivo CSV se cargó correctamente
df.columns = df.columns.str.strip()  # Eliminar espacios en blanco de los nombres de las columnas
print(df.describe(include="all"))  # Verificar que los datos se cargaron correctamente
print(df.columns.tolist())

# Configurar Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(template_path)

# Procesar cada empleado
def generar_imagen_segura(hti, html_content, output_filename):
    """Versión robusta del proceso de generación"""
    try:
        # Asegurar nombre de archivo válido
        safe_filename = "".join(c for c in output_filename if c.isalnum() or c in ('_', '-', '.'))
        # output_path = os.path.join(output_dir, safe_filename)
        
        # Generar usando directorio temporal controlado
        hti.screenshot(

            html_str=html_content,
            save_as=safe_filename,
            size=(328, 308),    
           
        )

        return True
    except Exception as e:
        print(f"Error al generar {output_filename}: {str(e)}")
        return False
def cortar_imagen(input_path, output_folder, size=(328, 208)):
    """Corta la imagen a un tamaño específico."""
    try:
        with Image.open(input_path) as img:
            img = img.resize(size, Image.ANTIALIAS)
            img.save(output_folder)
        return True
    except Exception as e:
        print(f"Error al cortar imagen {input_path}: {str(e)}")
        return False   

for _, empleado in df.iterrows():
    html_output = template.render(**empleado.to_dict())
    output_image = f"tarjeta_{empleado['Cédula']}{empleado['Nombres']}{empleado['Apellidos']}.png"
    
    if generar_imagen_segura(hti, html_output, output_image):
        # Cortar la imagen a un tamaño específico
       
        if cortar_imagen(output_image, output_folder + output_image):
            print(f"✓ Imagen cortada: {output_image}")
        print(f"✓ Imagen generada: {output_image}")
    else:
        print(f"✗ Falló generación para empleado {empleado['Cédula']}")

# for _, empleado in df.iterrows():
    # try:
        # html_output = template.render(**empleado.to_dict())
        # output_image = os.path.join(output_dir, f"tarjeta_{empleado['Cédula']}.png")
        # 
        # hti.screenshot(
            # html_str=html_output,
            # save_as=output_image
        # )
        # print(f"Imagen generada: {output_image}")
    # except Exception as e:
        # print(f"Error con empleado {empleado['Cédula']}: {str(e)}")

print("Proceso completado!")
