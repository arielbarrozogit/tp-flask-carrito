from flask import Flask, jsonify, request

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

@app.route('/')
def home():
    return "API Flask funcionando "

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


if __name__ == '__main__':
    app.run(debug=True)