
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class TransaccionesBase(SQLModel):
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)
    descripcion: Optional[str] = Field(default=None)


class TransaccionesCrear(TransaccionesBase):
    pass


class TransaccionesEditar(TransaccionesBase):
    pass


class Transacciones(TransaccionesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    factura_id: int | None = Field(default=None, foreign_key="factura.id")

    factura: Optional["Factura"] = Relationship(back_populates="transacciones")


class TransaccionLeer(TransaccionesBase):
    id: int