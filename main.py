from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear

app = FastAPI()


lista_clientes: list[Cliente] = []


# Endpoint para listar todos los clientes
@app.get("/clientes", response_model=list[Cliente])
def listar_clientes():
    return lista_clientes 


# Endpoint para listar un solo cliente de la lista
@app.get("/clientes/{cliente_id}", response_model=Cliente)
def listar_cliente(cliente_id: int):
    for obj_cliente in lista_clientes:
        if obj_cliente.id == cliente_id:
            return obj_cliente
        
# endpoint para crear un cliente
@app.post("/clientes", response_model=Cliente)
def crear_cliente(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    
    lista_clientes.append(cliente_val)
    return cliente_val