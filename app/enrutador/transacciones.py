from fastapi import APIRouter, HTTPException
from ..modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from ..modelos.facturas import Factura
from ..listas import lista_transacciones, lista_facturas

rutas_transacciones = APIRouter()



# Crear los endpoints para transacciones

@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones():
    return lista_transacciones


@rutas_transacciones.get("/transacciones/{id_transaccion}", response_model=Transaccion)
async def listar_transaccion(id_transaccion: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id_transaccion:
            return transaccion

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La transacción con id {id_transaccion} no existe"
    )

 # crear transacción
@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
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
@rutas_transacciones.patch("/transacciones/{id_transaccion}", response_model=Transaccion)
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
@rutas_transacciones.delete("/transacciones/{id_transaccion}", response_model=Transaccion)
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