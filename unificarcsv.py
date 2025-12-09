import pandas as pd
import glob
import os

def unificar_csv(directorio_archivos, nombre_archivo_salida):
    """
    Lee todos los archivos CSV en un directorio, los concatena en un solo
    DataFrame y lo guarda como un nuevo archivo CSV.

    Args:
        directorio_archivos (str): La ruta al directorio que contiene los archivos CSV.
        nombre_archivo_salida (str): El nombre del archivo CSV unificado de salida.
    """
    # 1. Encontrar todos los archivos CSV
    # Se utiliza glob.glob para encontrar todas las rutas que terminan en '.csv'
    ruta_busqueda = os.path.join(directorio_archivos, '*.csv')
    rutas_csv = glob.glob(ruta_busqueda)

    if not rutas_csv:
        print(f"❌ No se encontraron archivos CSV en el directorio: {directorio_archivos}")
        return

    print(f"✅ Se encontraron {len(rutas_csv)} archivos CSV para unificar.")

    # Lista para almacenar los DataFrames de cada archivo
    lista_dataframes = []

    # 2. Leer y almacenar cada archivo CSV
    for ruta in rutas_csv:
        try:
            # pd.read_csv lee el archivo
            # sep=',' es el valor por defecto, pero se incluye por claridad
            # encoding='utf-8' es un buen estándar, puedes cambiarlo si tus archivos usan otro
            df = pd.read_csv(ruta, sep=',', encoding='utf-8')
            lista_dataframes.append(df)
            print(f"   - Leído correctamente: {os.path.basename(ruta)}")
        except Exception as e:
            print(f"⚠️ Error al leer el archivo {os.path.basename(ruta)}: {e}")

    # 3. Concatenar todos los DataFrames
    # La función pd.concat() une los DataFrames.
    # El argumento 'ignore_index=True' restablece el índice de las filas unificadas.
    # MUY IMPORTANTE: La función 'concat' maneja automáticamente las columnas diferentes.
    # Si un archivo tiene una columna adicional, esa columna se crea en el DataFrame final,
    # y en los registros de los archivos que no la tienen, se llena con el valor **NaN**
    # (Not a Number, el valor de "valor faltante" de pandas).
    try:
        df_unificado = pd.concat(lista_dataframes, ignore_index=True)
        print("---")
        print("✅ DataFrames concatenados exitosamente.")
        print(f"Dimensiones del DataFrame final: {df_unificado.shape}")

    except Exception as e:
        print(f"❌ Error al concatenar los DataFrames: {e}")
        return

    # 4. Guardar el DataFrame unificado en un nuevo archivo CSV
    try:
        # index=False evita escribir los números de índice de pandas como una columna extra en el CSV.
        ruta_salida = os.path.join(directorio_archivos, nombre_archivo_salida)
        df_unificado.to_csv(ruta_salida, index=False, encoding='utf-8')
        print("---")
        print(f"🎉 Proceso finalizado. El archivo unificado se guardó en: **{ruta_salida}**")
        print("---")
    except Exception as e:
        print(f"❌ Error al guardar el archivo de salida: {e}")


# --- CONFIGURACIÓN Y EJECUCIÓN ---
# ⚠️ ADAPTA ESTAS DOS LÍNEAS ⚠️
directorio_csv = './csv carnets' # Cambia esto por la ruta de tu carpeta
archivo_salida = 'datos_unificados.csv'

# Crea el directorio si no existe (opcional, para prueba)
if not os.path.exists(directorio_csv):
    os.makedirs(directorio_csv)
    print(f"Se ha creado el directorio para colocar tus CSV: {directorio_csv}")
    print("Por favor, coloca tus archivos CSV dentro de esta carpeta y vuelve a ejecutar el script.")
else:
    # Llamada a la función principal
    unificar_csv(directorio_csv, archivo_salida)