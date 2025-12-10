import pyodbc

def diagnosticar_conexion():
    """Diagnóstico de conexión a SQL Server"""
    
    print("🔍 DIAGNÓSTICO DE CONEXIÓN SQL SERVER")
    print("=" * 40)
    
    # 1. Listar controladores ODBC disponibles
    print("\n1. Controladores ODBC disponibles:")
    drivers = pyodbc.drivers()
    for driver in drivers:
        print(f"   - {driver}")
    
    # 2. Probar diferentes configuraciones
    configuraciones = [
        {
            'name': 'Tu servidor MySQL (¿es SQL Server?)',
            'conn_str': (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=34.42.250.121;"
                "DATABASE=turflorapp;"
                "UID=desarrollo;"
                "PWD=DesTurFl2025*"
            )
        },
        {
            'name': 'SQL Server Local',
            'conn_str': (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost\\SQLEXPRESS;"
                "DATABASE=master;"
                "Trusted_Connection=yes;"
            )
        }
    ]
    
    print("\n2. Probando conexiones...")
    for config in configuraciones:
        print(f"\n   Probando: {config['name']}")
        try:
            conn = pyodbc.connect(config['conn_str'], timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"   ✅ CONEXIÓN EXITOSA!")
            print(f"   Versión: {version[:100]}...")
            conn.close()
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")

if __name__ == "__main__":
    diagnosticar_conexion()