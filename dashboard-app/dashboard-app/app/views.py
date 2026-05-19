from .extensions import appbuilder, db
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Categoria, Producto, Venta, DetalleVenta
from .ia_servicio import analizar_ventas
class CategoriaModelView(ModelView):
    datamodel = SQLAInterface(Categoria)
    label_columns = { "nombre" : "Nombre",
                    "descripcion": "Descripcion",
                    "imagen": "Imagen",
                    "estado": "Estado",
                    "creado_en": "Creado en",
                    "actualizado_en":"Actualizado en"}
    list_columns= ["nombre", "descripcion", "estado", "creado_en"]
    
    add_columns = ["nombre", "descripcion", "imagen", "estado"]
    edit_columns = ["nombre", "descripcion", "imagen", "estado"]
    show_columns = ["nombre", "descripcion", "imagen", "estado", "creado_en","actualizado_en"]
    
class ProductoModelView(ModelView):
    datamodel = SQLAInterface(Producto)
    label_columns = { "nombre" : "Nombre",
                    "descripcion": "Descripcion",
                    "precio" : "Precio",
                    "categorias": "Categoria",
                    "imagen": "Imagen",
                    "estado": "Estado",
                    "creado_en": "Creado en",
                    "actualizado_en":"Actualizado en"}
    list_columns= ["nombre", "precio", "categorias", "estado"]
    add_columns = ["nombre", "descripcion","precio","categorias", "imagen", "estado"]
    edit_columns = ["nombre", "descripcion","precio","categorias", "imagen", "estado"]
    show_columns = ["nombre", "descripcion", "precio", "imagen", "estado", "creado_en","actualizado_en"]
    
class VentaModelView(ModelView):
    datamodel = SQLAInterface(Venta)

    label_columns = {
        "id": "ID",
        "fecha": "Fecha",
        "total": "Total",
        "detalles": "Detalles"
    }

    list_columns = [
        "id",
        "fecha",
        "total"
    ]

    add_columns = [
        "total"
    ]

    edit_columns = [
        "total"
    ]

    show_columns = [
        "id",
        "fecha",
        "total",
        "detalles"
    ]
class DetalleVentaModelView(ModelView):
    datamodel = SQLAInterface(DetalleVenta)

    label_columns = {
        "venta": "Venta",
        "producto": "Producto",
        "cantidad": "Cantidad",
        "precio_unitario": "Precio Unitario",
        "subtotal": "Subtotal"
    }

    list_columns = [
        "venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]

    add_columns = [
        "venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]

    edit_columns = [
        "venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]
# REPORTES
class ReporteView(BaseView):
    route_base = '/reportes'    
    @expose("/")
    def index(self):
        total_ventas = db.session.query(Venta).count()
        total_ingresos = db.session.query(
                db.func.sum(Venta.total)
            ).scalar() or 0
        # venta_por_producto = db.session.query(
        #         Venta.producto,
        #         db.func.sum(Venta.cantidad)
        #     ).group_by(Venta.producto).all()
        venta_por_producto = db.session.query(
            Producto.nombre,
            db.func.sum(DetalleVenta.cantidad)
        ).join(
            DetalleVenta,
            Producto.id == DetalleVenta.producto_id
        ).group_by(
            Producto.nombre
        ).all()
        
        recomendacion_venta =""
        for producto, cantidad  in venta_por_producto:
            recomendacion_venta += f"{producto} : {cantidad}"
        
        analisis_venta = analizar_ventas(recomendacion_venta)
        return self.render_template("reportes.html",
                                    t_ventas = total_ventas,
                                    t_ingresos = total_ingresos,
                                    venta_por_producto = venta_por_producto,
                                    analisis_ia = analisis_venta
                                    )

appbuilder.add_view(
        CategoriaModelView,
        "Categorias",
        icon="fa-info",
        category="Configuraciones",
        category_icon="fa-info"
    )
    
appbuilder.add_view(
        ProductoModelView,
        "Productos",
        icon="fa-info",
        category="Configuraciones",
        category_icon="fa-info"
    )

appbuilder.add_view(
        VentaModelView,
        "Ventas",
        icon="fa-cart-arrow-down",
        category="Ventas",
        category_icon="fa-shopping-cart"
    )

appbuilder.add_view(
    DetalleVentaModelView,
    "Detalle Ventas",
    icon="fa-list",
    category="Ventas",
    category_icon="fa-shopping-cart"
)

appbuilder.add_view_no_menu(ReporteView())

appbuilder.add_link(
    "Reporte1",
    href="/reportes/",
    icon="fa-file-text",
    category="Reportes"
)