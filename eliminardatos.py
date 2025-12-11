import pandas as pd
from sqlalchemy import create_engine, text
import os

class MySQLDeleter:
    def __init__(self, host, database, username, password, port=3306):
        """
        Configura conexión a MySQL (Workbench)
        """
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.engine = None
    
    def create_connection(self):
        """Crea conexión a MySQL usando SQLAlchemy"""
        try:
            connection_string = (
                f"mysql+mysqlconnector://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.database}"
            )
            
            self.engine = create_engine(connection_string)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print("✅ Conexión a MySQL exitosa!")
            print(f"   Host: {self.host}:{self.port}")
            print(f"   Base de datos: {self.database}")
            print(f"   Usuario: {self.username}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión MySQL: {str(e)}")
            return False
    
    def read_csv_ids(self, csv_path, has_header=False):
        """
        Lee IDs desde CSV (columna A)
        """
        try:
            if has_header:
                df = pd.read_csv(csv_path)
                id_column = df.columns[0]
                ids = df[id_column].astype(str).str.strip().tolist()
            else:
                df = pd.read_csv(csv_path, header=None, names=['ID'])
                ids = df['ID'].astype(str).str.strip().tolist()
            
            # Filtrar valores vacíos y NaN
            ids = [str(id).strip() for id in ids if str(id).strip() and str(id).lower() != 'nan']
            
            print(f"\n📄 CSV procesado:")
            print(f"   Total filas leídas: {len(df)}")
            print(f"   IDs válidos encontrados: {len(ids)}")
            
            if len(ids) > 0:
                print(f"   Primeros 5 IDs: {ids[:5]}")
            
            return ids
            
        except Exception as e:
            print(f"❌ Error leyendo CSV: {str(e)}")
            return None
    
    def delete_records(self, table_name, id_column, ids):
        """
        Elimina registros donde id_column coincide con los IDs del CSV
        MÉTODO CORREGIDO: Usa parámetros nombrados correctamente
        """
        if not ids or self.engine is None:
            return 0
        
        try:
            with self.engine.connect() as conn:
                print(f"\n🔍 Verificando tabla '{table_name}'...")
                
                # 1. Verificar que la tabla existe
                check_table = text(f"SHOW TABLES LIKE :table_name")
                result = conn.execute(check_table, {'table_name': table_name})
                
                if not result.fetchone():
                    print(f"❌ La tabla '{table_name}' no existe")
                    return 0
                
                print(f"✅ Tabla '{table_name}' encontrada")
                
                # 2. Contar registros coincidentes
                print("📊 Contando registros coincidentes...")
                
                # Método 1: Contar uno por uno (más seguro)
                total_matches = 0
                for id_value in ids:
                    count_query = text(f"""
                        SELECT COUNT(*) 
                        FROM `{table_name}` 
                        WHERE `{id_column}` = :id_value
                    """)
                    result = conn.execute(count_query, {'id_value': id_value})
                    total_matches += result.scalar()
                
                print(f"🎯 {total_matches} registros coincidentes encontrados")
                
                if total_matches == 0:
                    print("ℹ️  No hay registros coincidentes para eliminar")
                    return 0
                
                # 3. Confirmar eliminación
                confirm = input(f"\n⚠️  ¿Eliminar {total_matches} registros de '{table_name}'? (si/no): ")
                if confirm.lower() not in ['si', 'sí', 's', 'yes', 'y']:
                    print("❌ Operación cancelada")
                    return 0
                
                # 4. Eliminar registros
                print("🗑️  Eliminando registros...")
                total_deleted = 0
                
                # Eliminar uno por uno (más controlado)
                for i, id_value in enumerate(ids, 1):
                    delete_query = text(f"""
                        DELETE FROM `{table_name}` 
                        WHERE `{id_column}` = :id_value
                    """)
                    
                    result = conn.execute(delete_query, {'id_value': id_value})
                    if result.rowcount > 0:
                        total_deleted += result.rowcount
                    
                    # Mostrar progreso cada 100 registros
                    if i % 100 == 0 or i == len(ids):
                        print(f"   Procesados: {i}/{len(ids)} IDs - Eliminados: {total_deleted}")
                
                conn.commit()
                print(f"\n✅ {total_deleted} registros eliminados exitosamente")
                
                return total_deleted
                
        except Exception as e:
            print(f"❌ Error durante la eliminación: {str(e)}")
            return 0

# ==============================================
# VERSIÓN MÁS EFICIENTE (usa parámetros nombrados)
# ==============================================
class MySQLDeleterEfficient:
    """
    Versión más eficiente para muchos registros
    """
    def __init__(self, host, database, username, password, port=3306):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.engine = None
    
    def create_connection(self):
        try:
            connection_string = (
                f"mysql+pymysql://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.database}"
            )
            self.engine = create_engine(connection_string)
            print("✅ Conexión a MySQL exitosa!")
            return True
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def delete_records_efficient(self, table_name, id_column, ids, batch_size=500):
        """
        Método eficiente usando parámetros nombrados dinámicamente
        """
        if not ids or self.engine is None:
            return 0
        
        try:
            with self.engine.connect() as conn:
                print(f"🎯 Eliminando registros de '{table_name}'...")
                
                # Procesar en lotes
                total_deleted = 0
                
                for i in range(0, len(ids), batch_size):
                    batch = ids[i:i + batch_size]
                    
                    # Crear parámetros nombrados dinámicamente
                    params = {}
                    conditions = []
                    
                    for idx, id_value in enumerate(batch):
                        param_name = f"id_{idx}"
                        params[param_name] = id_value
                        conditions.append(f":{param_name}")
                    
                    # Construir consulta con parámetros nombrados
                    where_clause = " OR ".join([f"`{id_column}` = {cond}" for cond in conditions])
                    delete_query = text(f"""
                        DELETE FROM `{table_name}` 
                        WHERE {where_clause}
                    """)
                    
                    # Ejecutar con diccionario de parámetros
                    result = conn.execute(delete_query, params)
                    deleted_in_batch = result.rowcount
                    total_deleted += deleted_in_batch
                    
                    conn.commit()
                    
                    # Mostrar progreso
                    processed = min(i + batch_size, len(ids))
                    print(f"   Lote {i//batch_size + 1}: {deleted_in_batch} eliminados ({processed}/{len(ids)})")
                
                print(f"\n✅ Total eliminados: {total_deleted}")
                return total_deleted
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return 0

# ==============================================
# VERSIÓN MÁS SIMPLE Y DIRECTA
# ==============================================
def eliminar_mysql_simple():
    """
    Versión simple y directa sin clases
    """
    # Configuración (usa tus datos)
    config = {
        'host': '34.42.250.121',
        'database': 'test-yeico',
        'username': 'desarrollo',
        'password': 'DesTurFl2025*',
        'csv_file': 'datos.csv',
        'table_name': 'logistica',
        'id_column': 'ID_cajaQR'
    }
    
    print("🚀 Eliminación simple de registros MySQL")
    
    # 1. Leer CSV (sin cabecera)
    try:
        df = pd.read_csv(config['csv_file'], header=None)
        ids = [str(id).strip() for id in df[0] if str(id).strip()]
        
        if not ids:
            print("⚠️  No hay IDs en el CSV")
            return
        
        print(f"📄 IDs encontrados: {len(ids)}")
        print(f"📋 Ejemplo: {ids[:5]}")
        
    except Exception as e:
        print(f"❌ Error leyendo CSV: {e}")
        return
    
    # 2. Conectar a MySQL
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{config['username']}:{config['password']}"
            f"@{config['host']}/{config['database']}"
        )
        
        print(f"🔗 Conectado a {config['host']}/{config['database']}")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Probando con pymysql...")
        try:
            engine = create_engine(
                f"mysql+pymysql://{config['username']}:{config['password']}"
                f"@{config['host']}/{config['database']}"
            )
        except Exception as e2:
            print(f"❌ También falló: {e2}")
            return
    
    # 3. Eliminar registros (método simple y seguro)
    try:
        with engine.connect() as conn:
            deleted_count = 0
            
            print(f"\n🗑️  Eliminando registros...")
            
            # Método seguro: uno por uno
            for i, id_value in enumerate(ids, 1):
                # Usar parámetros nombrados correctamente
                query = text(f"""
                    DELETE FROM `{config['table_name']}` 
                    WHERE `{config['id_column']}` = :id_val
                """)
                
                result = conn.execute(query, {'id_val': id_value})
                
                if result.rowcount > 0:
                    deleted_count += result.rowcount
                
                # Mostrar progreso
                if i % 100 == 0 or i == len(ids):
                    print(f"   Procesados: {i}/{len(ids)} - Eliminados: {deleted_count}")
            
            conn.commit()
            print(f"\n✅ Total eliminados: {deleted_count}")
            
    except Exception as e:
        print(f"❌ Error durante eliminación: {e}")

# ==============================================
# PROGRAMA PRINCIPAL
# ==============================================
def main():
    print("=" * 60)
    print("ELIMINADOR DE REGISTROS - MySQL Workbench")
    print("=" * 60)
    
    # Usando tus datos del script anterior
    CONFIG = {
        'host': '34.42.250.121',
        'port': 3306,
        'database': 'turflorapp',
        'username': 'desarrollo',
        'password': 'DesTurFl2025*',
        'csv_file': 'datos1.csv',
        'table_name': 'inventarioactivo',
        'id_column': 'ID_cajaQR'
    }
    
    # Preguntar si el CSV tiene cabecera
    has_header_input = input("¿El archivo CSV tiene línea de cabecera? (si/no): ")
    has_header = has_header_input.lower() in ['si', 'sí', 's', 'yes', 'y']
    
    # Crear instancia simple
    print("\n1. Conectando a MySQL...")
    deleter = MySQLDeleter(
        host=CONFIG['host'],
        database=CONFIG['database'],
        username=CONFIG['username'],
        password=CONFIG['password'],
        port=CONFIG['port']
    )
    
    if not deleter.create_connection():
        print("💡 Probando método alternativo...")
        eliminar_mysql_simple()
        return
    
    # Verificar archivo
    print("\n2. Verificando archivo...")
    if not os.path.exists(CONFIG['csv_file']):
        print(f"❌ Archivo no encontrado: {CONFIG['csv_file']}")
        return
    
    # Leer IDs
    print("\n3. Leyendo CSV...")
    ids = deleter.read_csv_ids(CONFIG['csv_file'], has_header)
    
    if not ids:
        return
    
    # Eliminar registros
    print("\n4. Eliminando registros...")
    deleted = deleter.delete_records(
        table_name=CONFIG['table_name'],
        id_column=CONFIG['id_column'],
        ids=ids
    )
    
    print("\n" + "=" * 50)
    print(f"RESUMEN: {deleted} registros eliminados")
    print("=" * 50)

# ==============================================
# EJECUCIÓN ALTERNATIVA: VERSIÓN RÁPIDA
# ==============================================
def ejecutar_version_rapida():
    """
    Ejecuta directamente la versión simple sin preguntas
    """
    print("⚡ EJECUTANDO VERSIÓN RÁPIDA ⚡")
    eliminar_mysql_simple()

if __name__ == "__main__":
    # Opción 1: Versión completa con confirmación
    main()
    
    # Opción 2: Versión rápida sin confirmaciones
    # ejecutar_version_rapida()