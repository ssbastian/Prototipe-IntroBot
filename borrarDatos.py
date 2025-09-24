import sqlite3

def vaciar_tabla():
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect("rasa.db")
        cursor = conexion.cursor()

        # Eliminar todos los registros de la tabla 'events'
        cursor.execute("DELETE FROM events;")

        # Guardar cambios
        conexion.commit()
        print("✅ La tabla 'events' ha sido vaciada correctamente.")

    except sqlite3.Error as e:
        print(f"❌ Error al vaciar la tabla: {e}")

    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    vaciar_tabla()
