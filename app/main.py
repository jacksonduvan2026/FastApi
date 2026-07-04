from fastapi import FastAPI

from app.enrutador import clientes
from app.enrutador import facturas
from app.enrutador import transacciones
from app.conexion_bd import crear_tablas

app = FastAPI(lifespan=crear_tablas)

app.include_router(clientes.rutas_clientes, tags=["Clientes"])
app.include_router(facturas.rutas_facturas, tags=["Facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["Transacciones"])


