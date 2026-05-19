import datetime
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Categoria(Model):
    __tablename__="categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime,  default=datetime.datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime,  default=datetime.datetime.utcnow, onupdate= datetime.UTC, nullable=False)

    productos = relationship(
        "Producto",
        back_populates="categorias"
    )
    
    def __repr__(self):
        return  self.nombre
    
class Producto(Model):
    __tablename__="producto"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    imagen = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime,  default=datetime.datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime,  default=datetime.datetime.utcnow, onupdate= datetime.UTC, nullable=False)
    categorias = relationship(
        "Categoria",
        back_populates="productos"
    )
    detalles_venta = relationship(
        "DetalleVenta",
        back_populates="producto",
        cascade="all, delete"
    )
    def __repr__(self):
        return  self.nombre

class Venta(Model):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True)

    fecha = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    total = Column(Numeric(10, 2), default=0)

    creado_en = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    detalles = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"Venta #{self.id}"
    
class DetalleVenta(Model):
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True)

    venta_id = Column(
        Integer,
        ForeignKey("venta.id"),
        nullable=False
    )

    producto_id = Column(
        Integer,
        ForeignKey("producto.id"),
        nullable=False
    )

    cantidad = Column(Integer, nullable=False)

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    venta = relationship(
        "Venta",
        back_populates="detalles"
    )

    producto = relationship(
        "Producto",
        back_populates="detalles_venta"
    )

    def __repr__(self):
        return f"{self.producto} - {self.cantidad}"