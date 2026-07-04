from pydantic import BaseModel

# Modelo base de transacción
class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float

# Modelo para crear una transacción
class TransaccionCrear(TransaccionBase):
    pass

# Modelo para editar una transacción
class TransaccionEditar(TransaccionBase):
    pass

# Modelo para responder una transacción
class Transaccion(TransaccionBase):
    id: int | None = None
    factura_id: int | None = None  # aqui va la relacion con el modelo factura(sol un campo )
    # aqui va la relacion con el modelo factura(sol un campo )