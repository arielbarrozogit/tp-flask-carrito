from flask import Flask, jsonify, request, render_template

# incorpore Render_template para poder renderizar un template HTML en el endpoint /productos_db

#Importo la función get_db desde el archivo db.py en diferencia al TP PASO 1
from db import get_db 


app = Flask(__name__)

# -------------------------
# DATOS EN MEMORIA
# -------------------------
productos = [
    {"id": 1, "nombre": "Café", "precio": 1200},
    {"id": 2, "nombre": "Medialuna", "precio": 800},
    {"id": 3, "nombre": "Tostado", "precio": 1500}
]

carrito = []

# -------------------------
# ENDPOINTS
# -------------------------
""" FUNCION ORIGINAL DEL  PASO 1 DEL TP
@app.route('/')
def home():
    return "API Flask funcionando del TP Programacion WEB 2 - Carrito de compras"
"""
#  listar productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    return jsonify(productos)

@app.route('/carrito', methods=['GET'])
def ver_carrito():

    resumen = {}
    total = 0

    for producto in carrito:

        id_producto = producto["id"]

        if id_producto not in resumen:
            resumen[id_producto] = {
                "id": producto["id"],
                "nombre": producto["nombre"],
                "precio_unitario": producto["precio"],
                "cantidad": 0,
                "subtotal": 0
            }

        resumen[id_producto]["cantidad"] += 1
        resumen[id_producto]["subtotal"] += producto["precio"]

        total += producto["precio"]

    return jsonify({
        "items": list(resumen.values()),
        "total": total
    })

@app.route('/carrito', methods=['POST'])
def agregar_carrito():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Debe enviar JSON"
        }), 400

    producto_id = data.get("id")

    producto = next(
        (p for p in productos if p["id"] == producto_id),
        None
    )

    if not producto:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404
    ## agrego con append al carrito un producto que es un diccionario con id, nombre y precio al FINAL del mismo 

    carrito.append(producto)

    return jsonify({
        "mensaje": "Producto agregado",
        "carrito": carrito
    })

@app.route('/carrito/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):

    for item in carrito:

        if item["id"] == id_producto:
            carrito.remove(item)

            return jsonify({
                "mensaje": "Producto eliminado"
            })

    return jsonify({
        "error": "Producto no encontrado en el carrito"
    }), 404

# AGREGO PASO2 del tp implementando persistencia de datos en el servidor Flask 

@app.route('/productos_db', methods=['GET'])
def listar_productos_db():

    conn = get_db()

    productos = conn.execute(
        "SELECT * FROM productos"
    ).fetchall()

    conn.close()

    return jsonify([
        dict(producto)
        for producto in productos
    ])

@app.route('/carrito_db', methods=['POST'])
def agregar_carrito_db():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Debe enviar JSON"
        }), 400

    producto_id = data.get("id")

    conn = get_db()

    producto = conn.execute(
        """
        SELECT *
        FROM productos
        WHERE id = ?
        """,
        (producto_id,)
    ).fetchone()

    if not producto:

        conn.close()

        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    conn.execute(
        """
        INSERT INTO carrito
        (producto_id, cantidad)
        VALUES (?, ?)
        """,
        (producto_id, 1)
    )

    conn.commit()

    conn.close()

    return jsonify({
        "mensaje": "Producto agregado en SQLite"
    })
@app.route('/carrito_db', methods=['GET'])
def ver_carrito_db():

    conn = get_db()

    items = conn.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            COUNT(*) AS cantidad,
            p.precio * COUNT(*) AS subtotal
        FROM carrito c
        INNER JOIN productos p
            ON c.producto_id = p.id
        GROUP BY
            p.id,
            p.nombre,
            p.precio
    """).fetchall()

    total = sum(item["subtotal"] for item in items)

    conn.close()

    return jsonify({
        "items": [
            {
                "id": item["id"],
                "nombre": item["nombre"],
                "precio_unitario": item["precio"],
                "cantidad": item["cantidad"],
                "subtotal": item["subtotal"]
            }
            for item in items
        ],
        "total": total
    })

@app.route('/carrito_db/<int:id_producto>', methods=['DELETE'])
def eliminar_producto_db(id_producto):

    conn = get_db()

    item = conn.execute(
        """
        SELECT id
        FROM carrito
        WHERE producto_id = ?
        LIMIT 1
        """,
        (id_producto,)
    ).fetchone()

    if not item:

        conn.close()

        return jsonify({
            "error": "Producto no encontrado en el carrito"
        }), 404

    conn.execute(
        """
        DELETE FROM carrito
        WHERE id = ?
        """,
        (item["id"],)
    )

    conn.commit()

    conn.close()

    return jsonify({
        "mensaje": "Producto eliminado"
    })

@app.route('/carrito_db', methods=['DELETE'])
def vaciar_carrito():

    conn = get_db()

    conn.execute("DELETE FROM carrito")

    conn.commit()

    conn.close()

    return jsonify({
        "mensaje": "Carrito vaciado"
    })

# aca ya no es endpoint, sino que, es la ruta que renderiza el template index.html, que es el front end del carrito de compras

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)