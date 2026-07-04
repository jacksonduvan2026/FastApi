from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, computed_field
from app.modelos.clientes import Cliente, ClienteLeer
from ..modelos.transacciones import Transacciones


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now ())
    
    
    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0

        if not hasattr(self, "transacciones") or not self.transacciones:
            return total_factura

        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura

   
        
class FacturaCrear(FacturaBase):
    
    pass

class FacturaEditar(BaseModel):
    cliente_id: int | None = None
    pass

class Factura(FacturaBase):
    id: int | None = None

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True )
    cliente_id: int= Field(default=None, foreign_key="cliente.id")
    cliente : Cliente = Relationship(back_populates="factura")
    transacciones: list[Transacciones] = Relationship(back_populates="factura")

class FacturaLeer(FacturaBase): 
    id: int
    cliente: ClienteLeer
    #transacciones: list[Transacciones]=[]

class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[Transacciones]=[]