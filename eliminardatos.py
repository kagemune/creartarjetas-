import pandas as pd
import pyodbc

def eliminar_por_csv_simple():
    # CONFIGURACIÓN RÁPIDA
    SERVER = "'34.42.250.121'"
    DATABASE = "turflorapp"
    USERNAME = "desarrollo"
    PASSWORD = "DesTurFl2025*"
    CSV_FILE = "datos.csv"  # CSV sin cabeceras
    TABLA = "inventarioactivo"

    
    # 1. Leer CSV (solo columna A)
    print("Leyendo CSV...")
    df = pd.read_csv(CSV_FILE, header=None)
    ids = df[0].astype(str).str.strip().tolist()
    ids = [id for id in ids if id]  # Filtrar vacíos
    
    print(f"IDs encontrados: {len(ids)}")
    print(f"Ejemplo: {ids[:5]}")
    
    if not ids:
        print("No hay datos en el CSV")
        return
    
    # 2. Conectar a SQL Server
    print("Conectando a SQL Server...")
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # 3. Eliminar en lotes
    print("Eliminando registros...")
    lote = 1000
    eliminados = 0
    
    for i in range(0, len(ids), lote):
        batch = ids[i:i + lote]
        placeholders = ','.join(['?' for _ in batch])
        
        query = f"""
            DELETE FROM {TABLA} 
            WHERE CAST(ID_CajaQR AS VARCHAR(255)) IN ({placeholders})
        """
        
        cursor.execute(query, batch)
        eliminados += cursor.rowcount
        conn.commit()
        
        print(f"  Lote {i//lote + 1}: {cursor.rowcount} eliminados")
    
    print(f"\n✅ Total eliminados: {eliminados}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    eliminar_por_csv_simple()