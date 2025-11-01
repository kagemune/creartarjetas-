from PIL import Image
import os
from pathlib import Path

def procesar_imagen(ruta_entrada, ruta_salida):
    try:
        # Convertir a Path object
        entrada = Path(ruta_entrada)
        salida = Path(ruta_salida)
        
        # Verificar existencia
        if not entrada.exists():
            raise FileNotFoundError(f"Archivo origen no existe: {entrada}")
        
        # Procesar imagen
        with Image.open(entrada) as img:
            img_rgb = img.convert('RGB')  # mantener a color 
            img_rgb.save(salida, quality=95)  # Guardar con calidad 95
            area = (26, 18, 330, 597)  # Ajusta estos valores
            cropped_img = img_rgb.crop(area)
            cropped_img.save(salida, quality=95)
            # Imprimir mensaje de éxito
            
        print(f"Imagen procesada y guardada en: {salida}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

#declarar directorios de entrada y salida
dirEntrada = "./tarjetas/"
dirSalida  = "./resultados/"

for img in os.listdir(dirEntrada):
    if img.endswith(".jpg") or img.endswith(".png"):
        procesar_imagen(
            ruta_entrada=os.path.join(dirEntrada, img),
            ruta_salida= os.path.join(dirSalida, img)
        )

