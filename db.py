import sqlite3

DB_NAME = "carrito.db"

def get_db():
    """
    Devuelvo una conexión SQLite.
    """

    # Uso CONN en lugar de escribir todos los endpoints
    conn = sqlite3.connect(DB_NAME)

    # Permite acceder por nombre de columna
    conn.row_factory = sqlite3.Row

    return conn