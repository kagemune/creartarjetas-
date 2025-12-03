import pandas as pd
from io import StringIO

# Leer el contenido CSV
df = pd.read_csv(StringIO(file_content))

# Obtener cod_clas únicos por fecha
unique_codes_by_date = df.groupby('fecha')['cod_clas'].unique()

# Preparar datos para CSV
csv_data = []
for fecha, codigos in unique_codes_by_date.items():
    csv_data.append({'fecha': fecha, 'cod_clas': '--- INICIO FECHA ---'})
    for codigo in codigos:
        csv_data.append({'fecha': '', 'cod_clas': codigo})
    csv_data.append({'fecha': '', 'cod_clas': '--- FIN FECHA ---'})
    csv_data.append({'fecha': '', 'cod_clas': ''})  # Línea en blanco

# Crear DataFrame para CSV
csv_df = pd.DataFrame(csv_data)
# 
# Guardar como CSV
csv_output = csv_df.to_csv(index=False, encoding='utf-8')

print("✅ CSV generado exitosamente!")
print(f"Total de fechas procesadas: {len(unique_codes_by_date)}")
print(f"Total de registros en el CSV: {len(csv_data)}")
print("\nPrimeras 20 líneas del CSV:")
print(csv_output.split('\n')[:20])