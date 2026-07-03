from pydantic import BaseModel, computed_field
from .transacciones import Transaccion
from .clientes import Cliente
from datetime import datetime

# Modelo base de factura
class FacturaBase(BaseModel):
    fecha: str = datetime.now()
    cliente: Cliente
    transacciones: list[Transaccion] = []
    
    @computed_field
    @property
    def vr_total(self) -> float:
        # calcular(cantidad * vr_unitario) 
        return 222
    
# Modelo para crear una factura
class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

# Modelo para responder una factura
class Factura(FacturaBase):
    id: int | None = None