from PIL import Image, ImageDraw
import os

# Crear carpeta assets si no existe
os.makedirs('assets', exist_ok=True)

# Crear una imagen simple de 64x64 píxeles
img = Image.new('RGB', (64, 64), color='#2196F3')
draw = ImageDraw.Draw(img)

# Dibujar una tarjeta simple
draw.rectangle([10, 15, 50, 54], outline='white', width=2)
draw.text((17, 35), "Card", fill='white')

# Guardar como icono
img.save('assets/icono.ico', format='ICO')

print("Icono creado exitosamente en assets/icono.ico")