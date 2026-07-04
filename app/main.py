from fastapi import FastAPI, HTTPException, status
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
app = FastAPI()


lista_clientes: list[Cliente] = [] 
lista_facturas: list[Factura] = []
lista_transacciones: list[Transaccion] = []


# Endpoint para obtener o listar todos los clientes
@app.get("/clientes", response_model=list[Cliente])
async def listar_clientes():
    return lista_clientes 


# Endpoint para obtener o listar un solo cliente de la lista
@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int):
    for obj_cliente in lista_clientes:
        if obj_cliente.id == cliente_id:
            return obj_cliente
    raise HTTPException(
        status_code=400, detail=f"El cliente con id {cliente_id} no existe"
    )

        
# endpoint para crear un cliente, y agregar a la lista
@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    # generar id
    id_cliente= len(lista_clientes) + 1
    cliente_val.id = id_cliente
    lista_clientes.append(cliente_val)
    return cliente_val


# endpoint para editar un cliente, y agregar a la lista
@app.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            # validar cliente
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = cliente_id
            lista_clientes[i] = cliente_val
            return cliente_val
    raise HTTPException(status_code=400 , detail=f"El Cliente con id {cliente_id} no existe"
    )    
    
    
    # Endpoint para eliminar un cliente
@app.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            cliente_eliminado = lista_clientes.pop(i)
            return cliente_eliminado

    raise HTTPException(
        status_code=400,
        detail=f"El cliente con id {cliente_id} no existe"
    )
    
#crear los endpoints para facturas
    
@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas


@app.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id: int):
    # recorrer la lista_factura
    for obj_factura in lista_facturas:
        if obj_factura.id == factura_id:
            return obj_factura
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La factura con id {factura_id} no existe"
    )

@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear):
    #buscar el cliente
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
    # mensaje si no existe el cliente 
    if not cliente_encontrado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id} no existe"
        )
        
    #validar datos de la factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.cliente = cliente_encontrado
    # id de la factura
    factura_val.id = len(lista_facturas) + 1
    lista_facturas.append(factura_val)
    return factura_val
   

@app.patch("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaEditar):
    pass


@app.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int):
    pass
 

# Crear los endpoints para transacciones

@app.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones():
    return lista_transacciones


@app.get("/transacciones/{id_transaccion}", response_model=Transaccion)
async def listar_transaccion(id_transaccion: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id_transaccion:
            return transaccion

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La transacción con id {id_transaccion} no existe"
    )

 # crear transacción
@app.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    # buscar la factura
    factura_encontrada = None

    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura

    # mensaje si no existe la factura
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id} no existe"
        )

    # validar los datos de la transacción
    transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_val.factura_id = factura_id

    # id de la transacción
    transaccion_val.id = len(lista_transacciones) + 1

    # agregar a la lista general
    lista_transacciones.append(transaccion_val)

    # agregar a la factura
    factura_encontrada.transacciones.append(transaccion_val)
    return transaccion_val
    

# editar transaccion
@app.patch("/transacciones/{id_transaccion}", response_model=Transaccion)
async def editar_transaccion(id_transaccion: int, datos_transaccion: TransaccionEditar):
    for i, obj_transaccion in enumerate(lista_transacciones):
        if obj_transaccion.id == id_transaccion:
            # validar transacción
            transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
            transaccion_val.id = id_transaccion
            transaccion_val.factura_id = obj_transaccion.factura_id

            # actualizar lista de transacciones
            lista_transacciones[i] = transaccion_val

            # actualizar la transacción dentro de la factura
            for factura in lista_facturas:
                if factura.id == transaccion_val.factura_id:
                    for j, transaccion in enumerate(factura.transacciones):
                        if transaccion.id == id_transaccion:
                            factura.transacciones[j] = transaccion_val
                            break

            return transaccion_val

    raise HTTPException(
        status_code=400,
        detail=f"La Transacción con id {id_transaccion} no existe"
    )
 
# eliminar transaccion
@app.delete("/transacciones/{id_transaccion}", response_model=Transaccion)
async def eliminar_transaccion(id_transaccion: int):
    for i, obj_transaccion in enumerate(lista_transacciones):
        if obj_transaccion.id == id_transaccion:

            # eliminar de la lista de transacciones
            transaccion_eliminada = lista_transacciones.pop(i)

            # eliminar de la factura correspondiente
            for factura in lista_facturas:
                if factura.id == transaccion_eliminada.factura_id:
                    for j, transaccion in enumerate(factura.transacciones):
                        if transaccion.id == id_transaccion:
                            factura.transacciones.pop(j)
                            break

            return transaccion_eliminada

    raise HTTPException(
        status_code=400,
        detail=f"La Transacción con id {id_transaccion} no existe"
    )