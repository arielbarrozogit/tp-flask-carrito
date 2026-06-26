window.onload = () => {

    cargarProductos();
    cargarCarrito();

}

async function cargarProductos(){

    const response =
        await fetch('/productos_db');

    const productos =
        await response.json();

    const contenedor =
        document.getElementById('productos');

    contenedor.innerHTML = '';

    productos.forEach(producto => {

        contenedor.innerHTML += `

            <div class="col-md-4">

                <div class="card card-producto">

                    <div class="card-body text-center">

                        <h1>☕</h1>

                        <h5>${producto.nombre}</h5>

                        <p>$${producto.precio}</p>

                        <button
                            class="btn btn-success"
                            onclick="agregar(${producto.id})"
                        >
                            Agregar
                        </button>

                    </div>

                </div>

            </div>

        `;
    });

}


async function agregar(id){

    await fetch('/carrito_db',{

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify({
            id:id
        })
    });

   // alert('Producto agregado'); esto funcionaba antes pero no refresca el carrito
   await cargarCarrito(); 

}

async function cargarCarrito(){

    const response =
        await fetch('/carrito_db');

    const data =
        await response.json();

    const carrito =
        document.getElementById('carrito');

    carrito.innerHTML = '';

    data.items.forEach(item => {

        carrito.innerHTML += `

           
<div class="d-flex justify-content-between align-items-center border-bottom py-2">

        <div>
            ☕ ${item.nombre}
            x ${item.cantidad}
        </div>

        <div>

            <span class="me-2">
                $${item.subtotal}
            </span>

            <button
                class="btn btn-sm btn-danger"
                onclick="eliminar(${item.id})"
            >
                🗑️
            </button>

        </div>

    </div>

        `;

});
 document.getElementById('total').innerHTML =
        `Total: $${data.total}`;

}
async function eliminar(id){

    await fetch(`/carrito_db/${id}`,{
        method:'DELETE'
    });

    await cargarCarrito();

}

async function vaciarCarrito(){

    if(!confirm("¿Desea vaciar todo el carrito?")){
        return;
    }

    await fetch('/carrito_db',{
        method:'DELETE'
    });

    await cargarCarrito();

}
   

