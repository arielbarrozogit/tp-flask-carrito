import sqlite3

# Crear o abrir la base
conn = sqlite3.connect("carrito.db")

cursor = conn.cursor()

# Tabla productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)
""")

# Tabla carrito
cursor.execute("""
CREATE TABLE IF NOT EXISTS carrito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 1,
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
""")

# Productos iniciales
productos = [
    (1, "Café", 1200),
    (2, "Medialuna", 800),
    (3, "Tostado", 1500)
]

cursor.executemany("""
INSERT OR IGNORE INTO productos
(id, nombre, precio)
VALUES (?, ?, ?)
""", productos)

conn.commit()
conn.close()

print("✅ Base creada correctamente")