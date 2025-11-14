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
            img_gris = img.convert('L')  # Convertir a escala de grises
            img_gris.save(salida)
            area = (3, 1, 412, 210)  # Ajusta estos valores
            cropped_img = img_gris.crop(area)
            cropped_img.save(salida)
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

