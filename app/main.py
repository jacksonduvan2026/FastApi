from fastapi import FastAPI

from app.enrutador import clientes
from app.enrutador import facturas
from app.enrutador import transacciones

app = FastAPI()

#incluir ruta de clientes
app.include_router(clientes.rutas_clientes, tags=["Clientes"])
app.include_router(facturas.rutas_facturas, tags=["Facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["Transacciones"])







