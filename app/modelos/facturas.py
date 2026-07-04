from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, computed_field
from app.modelos.clientes import Cliente, ClienteLeer
from ..modelos.transacciones import Transacciones


# Modelo base de factura
class FacturaBase(BaseModel):
    fecha: str = datetime.now()
    cliente: Cliente
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def vr_total(self) -> float:
        # calcular (cantidad * vr_unitario)
        # consultar el id actual de la factura
        factura_id_actual = getattr(self, "id", None)
        total_factura = 0.0

        if factura_id_actual is None or not self.transacciones:
            return total_factura

        # recorrer la lista de transacciones según el factura_id
        for transaccion in self.transacciones:
            if transaccion.factura_id == factura_id_actual:
                total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura


# Modelo para crear una factura
class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


# Modelo para responder una factura
class Factura(FacturaBase):
    id: int | None = None