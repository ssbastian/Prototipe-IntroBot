import sqlite3
import pandas as pd

def exportar_encuestas_csv(nombre_csv="encuestas.csv"):
    conn = sqlite3.connect("usuarios.db")

    # Leer la tabla encuestas en un DataFrame
    df = pd.read_sql_query("SELECT * FROM encuestas", conn)

    # Guardar en CSV
    df.to_csv(nombre_csv, index=False, encoding="utf-8")

    conn.close()
    print(f"✅ Archivo CSV generado: {nombre_csv}")


# Ejemplo de uso
exportar_encuestas_csv()
