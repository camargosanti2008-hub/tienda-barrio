import flet as ft

from data.cliente_dao import ClienteDAO
from data.producto_repository import ProductoRepository
from data.venta_dao import VentaDAO
from domain.venta import Venta


class VentasView:
    """Pantalla de ventas: se escoge cliente y producto con Dropdown y se escribe la cantidad."""

    def __init__(self, page: ft.Page, venta_dao: VentaDAO,
                 cliente_dao: ClienteDAO, producto_repo: ProductoRepository) -> None:
        self.page = page
        self.venta_dao = venta_dao
        self.cliente_dao = cliente_dao
        self.producto_repo = producto_repo
        self.id_editando = None

        # ---- Formulario ----
        self.dd_cliente = ft.Dropdown(label="Cliente", width=250, options=[])
        self.dd_producto = ft.Dropdown(label="Producto", width=250, options=[])
        self.txt_cantidad = ft.TextField(label="Cantidad", width=120, keyboard_type=ft.KeyboardType.NUMBER)
        self.btn_guardar = ft.ElevatedButton("Registrar venta", icon=ft.Icons.SHOPPING_CART, on_click=self.guardar)
        self.btn_limpiar = ft.OutlinedButton("Limpiar", on_click=self.limpiar)
        self.mensaje = ft.Text("")
        self.lbl_total = ft.Text("")

        # ---- Tabla ----
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
        )

    def construir(self) -> ft.Control:
        self.cargar_opciones()
        self.cargar_tabla()
        return ft.Column(
            [
                ft.Text("Ventas", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.dd_cliente, self.dd_producto, self.txt_cantidad], wrap=True),
                ft.Row([self.btn_guardar, self.btn_limpiar]),
                self.mensaje,
                self.lbl_total,
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def cargar_opciones(self) -> None:
        """Llena los Dropdown con los clientes y productos que hay en la BD."""
        self.dd_cliente.options = [
            ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in self.cliente_dao.listar()
        ]
        self.dd_producto.options = [
            ft.dropdown.Option(key=str(p.id), text=f"{p} - stock: {p.stock}") for p in self.producto_repo.listar()
        ]

    def cargar_tabla(self) -> None:
        self.lbl_total.value = f"Total de ventas: {len(self.venta_dao)}"
        self.tabla.rows.clear()
        for venta in self.venta_dao.listar():
            self.tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(venta.id))),
                    ft.DataCell(ft.Text(venta.cliente_nombre)),
                    ft.DataCell(ft.Text(venta.producto_nombre)),
                    ft.DataCell(ft.Text(str(venta.cantidad))),
                    ft.DataCell(ft.Text(f"${venta.total:,.0f}")),
                    ft.DataCell(ft.Text(venta.fecha)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE,
                                      on_click=lambda e, v=venta: self.editar(v)),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                      on_click=lambda e, v=venta: self.eliminar(v)),
                    ])),
                ])
            )

    def mostrar_mensaje(self, texto: str, es_error: bool = False) -> None:
        self.mensaje.value = texto
        self.mensaje.color = ft.Colors.RED if es_error else ft.Colors.GREEN

    def guardar(self, e) -> None:
        # ---- Validaciones ----
        if not self.dd_cliente.value or not self.dd_producto.value:
            self.mostrar_mensaje("Seleccione un cliente y un producto", es_error=True)
            self.page.update()
            return
        try:
            cantidad = int(self.txt_cantidad.value)
        except (ValueError, TypeError):
            self.mostrar_mensaje("La cantidad debe ser un número entero", es_error=True)
            self.page.update()
            return

        try:
            venta = Venta(
                cliente_id=int(self.dd_cliente.value),
                producto_id=int(self.dd_producto.value),
                cantidad=cantidad,
                id=self.id_editando,
            )
            if self.id_editando is None:
                self.venta_dao.crear(venta)
                self.mostrar_mensaje("Venta registrada correctamente")
            else:
                self.venta_dao.actualizar(venta)
                self.mostrar_mensaje("Venta actualizada correctamente")
            self.limpiar_campos()
            self.refrescar()
        except ValueError as error:  # cantidad <= 0, stock insuficiente, etc.
            self.mostrar_mensaje(str(error), es_error=True)
            self.page.update()

    def editar(self, venta: Venta) -> None:
        self.id_editando = venta.id
        self.dd_cliente.value = str(venta.cliente_id)
        self.dd_producto.value = str(venta.producto_id)
        self.txt_cantidad.value = str(venta.cantidad)
        self.mostrar_mensaje(f"Editando: {venta}")
        self.page.update()

    def eliminar(self, venta: Venta) -> None:
        self.venta_dao.eliminar(venta.id)  # también devuelve el stock al producto
        self.mostrar_mensaje(f"Venta #{venta.id} eliminada (stock devuelto)")
        self.refrescar()

    def limpiar_campos(self) -> None:
        self.id_editando = None
        self.dd_cliente.value = None
        self.dd_producto.value = None
        self.txt_cantidad.value = ""

    def limpiar(self, e) -> None:
        self.limpiar_campos()
        self.mostrar_mensaje("")
        self.page.update()

    def refrescar(self) -> None:
        self.cargar_opciones()   # el stock cambió, se actualiza el texto del Dropdown
        self.cargar_tabla()
        self.page.update()
