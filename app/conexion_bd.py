from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

#motor de bd
motor_bd = create_engine(url_bd)

#definir el metodo para crear las tablas
def crear_tablas(app:FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield # no hay nada para retornar o ejecutar

#definir el metod para la sesion
def obtener_sesion():
    with Session(motor_bd) as sesion:
        yield sesion#retorna la sesion

#denominado inyeccion de dependencias
#registrar la sesion como dependencia, utilizada en nuestros endpoints
sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]