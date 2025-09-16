## Conexión con la base de datos
##

import sqlite3

def guardarUsuario(sender_id: str, nombre: str):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            sender_id TEXT PRIMARY KEY,
            nombre TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO usuarios (sender_id, nombre)
        VALUES (?, ?)
        ON CONFLICT(sender_id) DO UPDATE SET
            nombre = excluded.nombre
    """, (sender_id, nombre))
    conn.commit()
    conn.close()
    
    
def guardarEncuesta(sender_id: str, slot_name: str, slot_mejora: str, slot_satisfaccion: str, slot_recomendacion: str):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # TAbla para guardar las encuestas 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id TEXT,
            slot_name TEXT,
            slot_mejora TEXT,
            slot_satisfaccion TEXT,
            slot_recomendacion TEXT,
            FOREIGN KEY (sender_id) REFERENCES usuarios(sender_id)
        )
    """)

    # Insertar los datos de la encuesta
    cursor.execute("""
        INSERT INTO encuestas (sender_id, slot_name, slot_mejora, slot_satisfaccion, slot_recomendacion)
        VALUES (?, ?, ?, ?, ?)
    """, (sender_id, slot_name, slot_mejora, slot_satisfaccion, slot_recomendacion))

    conn.commit()
    conn.close()