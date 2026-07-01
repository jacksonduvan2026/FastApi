from fastapi import FastAPI HTTPException
from pydantic import BaseModel

app = FastAPI()


#crear el modelo clientes(idm nombre, email, descripcion)
class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    descripcion: str


lista_clientes: list[Cliente] = []


# Endpoint para listar todos los clientes
@app.get("/clientes")
def listar_clientes():
    return lista_clientes 

# Endpoint para listar un solo cliente
@app.get("/clientes/{cliente_id}")
def listar_cliente(cliente_id: int):
    for obj_cliente in lista_clientes:
        if obj_cliente.get("id") == cliente_id:
            return obj_cliente
        
# endpoint para crear un cliente
@app.post("/clientes")
def crear_cliente(cliente: Cliente):
    lista_clientes.append(datos_cliente)
    return cliente
    