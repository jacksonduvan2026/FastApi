from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager

from modelos.clientes import Cliente
from modelos.facturas import Factura
from modelos.transacciones import Transaccion

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

motor_bd = create_engine(
    url_bd,
    connect_args={"check_same_thread": False}
)

@asynccontextmanager
async def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield

app = FastAPI(lifespan=crear_tablas)

def obtener_sesion():
    with Session(motor_bd) as sesion:
        yield sesion

sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]