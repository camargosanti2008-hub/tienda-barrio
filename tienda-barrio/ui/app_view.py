import flet as ft

from data.cliente_dao import ClienteDAO
from data.producto_repository import ProductoRepository
from data.venta_dao import VentaDAO
from ui.components.clientes_view import ClientesView
from ui.components.productos_view import ProductosView
from ui.components.ventas_view import VentasView


class AppView:
    """Ventana principal: un menú de botones arriba y el contenido de la pantalla elegida abajo."""

    def __init__(self, page: ft.Page, ruta_db: str) -> None:
        self.page = page
        self.page.title = "Tienda de Barrio La Esquina"
        self.page.padding = 20

        # Se crean los DAO (capa de datos) y se le pasan a cada pantalla
        cliente_dao = ClienteDAO(ruta_db)
        producto_repo = ProductoRepository(ruta_db)
        venta_dao = VentaDAO(ruta_db)

        self.vista_clientes = ClientesView(page, cliente_dao)
        self.vista_productos = ProductosView(page, producto_repo)
        self.vista_ventas = VentasView(page, venta_dao, cliente_dao, producto_repo)

        # Aquí se mostrará la pantalla seleccionada
        self.contenido = ft.Container(expand=True)

        menu = ft.Row([
            ft.ElevatedButton("Clientes", icon=ft.Icons.PEOPLE,
                              on_click=lambda e: self.mostrar(self.vista_clientes)),
            ft.ElevatedButton("Productos", icon=ft.Icons.INVENTORY,
                              on_click=lambda e: self.mostrar(self.vista_productos)),
            ft.ElevatedButton("Ventas", icon=ft.Icons.POINT_OF_SALE,
                              on_click=lambda e: self.mostrar(self.vista_ventas)),
        ])

        self.page.add(
            ft.Text("Tienda de Barrio La Esquina", size=28, weight=ft.FontWeight.BOLD),
            menu,
            ft.Divider(),
            self.contenido,
        )
        self.mostrar(self.vista_clientes)  # pantalla inicial

    def mostrar(self, vista) -> None:
        """Cambia la pantalla que se ve."""
        self.contenido.content = vista.construir()
        self.page.update()
