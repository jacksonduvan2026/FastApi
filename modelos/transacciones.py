from pydantic import BaseModel

# Modelo base de transacción
class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    id_factura: int

# Modelo para crear una transacción
class TransaccionCreate(TransaccionBase):
    pass

# Modelo para responder una transacción
class Transaccion(TransaccionBase):
    id: int | None = None