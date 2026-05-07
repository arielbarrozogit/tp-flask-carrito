"""
+++++VERSION 0
!primer codigo para probar que levanta app.run! ariel 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "API Flask funcionando ✅"

if __name__ == '__main__':
    app.run(debug=True)
    #
"""
""" +++++VERSION 1
from flask import Flask, jsonify

app = Flask(__name__)

# Productos en memoria
productos = [
    {"id": 1, "nombre": "Café", "precio": 1200},
    {"id": 2, "nombre": "Medialuna", "precio": 800},
    {"id": 3, "nombre": "Tostado", "precio": 1500}
]

@app.route('/')
def home():
    return "API Flask funcionando, requermiento Prog.Web2 (UNO)✅"

# ✅ endpoint productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True)
"""

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
    return "API Flask funcionando ✅"

# ✅ listar productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    return jsonify(productos)


# ✅ agregar al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    data = request.json
    producto_id = data.get("id")

    producto = next((p for p in productos if p["id"] == producto_id), None)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    carrito.append(producto)

    return jsonify({
        "mensaje": "Producto agregado",
        "carrito": carrito
    })


if __name__ == '__main__':
    app.run(debug=True)