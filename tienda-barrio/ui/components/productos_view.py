import sqlite3

import flet as ft

from data.producto_repository import ProductoRepository
from domain.producto import Producto


class ProductosView:
    """Pantalla de productos (inventario de la tienda)."""

    def __init__(self, page: ft.Page, repo: ProductoRepository) -> None:
        self.page = page
        self.repo = repo
        self.id_editando = None

        # ---- Formulario ----
        self.txt_nombre = ft.TextField(label="Nombre del producto", width=250)
        self.txt_precio = ft.TextField(label="Precio", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        self.txt_stock = ft.TextField(label="Stock", width=120, keyboard_type=ft.KeyboardType.NUMBER)
        self.btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar)
        self.btn_limpiar = ft.OutlinedButton("Limpiar", on_click=self.limpiar)
        self.mensaje = ft.Text("")
        self.lbl_total = ft.Text("")

        # ---- Tabla ----
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Stock")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
        )

    def construir(self) -> ft.Control:
        self.cargar_tabla()
        return ft.Column(
            [
                ft.Text("Productos", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.txt_nombre, self.txt_precio, self.txt_stock], wrap=True),
                ft.Row([self.btn_guardar, self.btn_limpiar]),
                self.mensaje,
                self.lbl_total,
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def cargar_tabla(self) -> None:
        self.lbl_total.value = f"Total de productos: {len(self.repo)}"
        self.tabla.rows.clear()
        for producto in self.repo.listar():
            self.tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(producto.id))),
                    ft.DataCell(ft.Text(producto.nombre)),
                    ft.DataCell(ft.Text(f"${producto.precio:,.0f}")),
                    ft.DataCell(ft.Text(str(producto.stock))),
                    ft.DataCell(ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE,
                                      on_click=lambda e, p=producto: self.editar(p)),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                      on_click=lambda e, p=producto: self.eliminar(p)),
                    ])),
                ])
            )

    def mostrar_mensaje(self, texto: str, es_error: bool = False) -> None:
        self.mensaje.value = texto
        self.mensaje.color = ft.Colors.RED if es_error else ft.Colors.GREEN

    def guardar(self, e) -> None:
        try:
            # float() e int() lanzan ValueError si escriben letras
            precio = float(self.txt_precio.value)
            stock = int(self.txt_stock.value)
        except (ValueError, TypeError):
            self.mostrar_mensaje("Precio y stock deben ser números", es_error=True)
            self.page.update()
            return

        try:
            producto = Producto(nombre=self.txt_nombre.value, precio=precio, stock=stock, id=self.id_editando)
            if self.id_editando is None:
                self.repo.crear(producto)
                self.mostrar_mensaje("Producto creado correctamente")
            else:
                self.repo.actualizar(producto)
                self.mostrar_mensaje("Producto actualizado correctamente")
            self.limpiar_campos()
            self.refrescar()
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            self.page.update()

    def editar(self, producto: Producto) -> None:
        self.id_editando = producto.id
        self.txt_nombre.value = producto.nombre
        self.txt_precio.value = str(int(producto.precio))
        self.txt_stock.value = str(producto.stock)
        self.mostrar_mensaje(f"Editando: {producto}")
        self.page.update()

    def eliminar(self, producto: Producto) -> None:
        try:
            self.repo.eliminar(producto.id)
            self.mostrar_mensaje(f"Producto '{producto.nombre}' eliminado")
        except sqlite3.IntegrityError:
            self.mostrar_mensaje("No se puede eliminar: el producto tiene ventas registradas", es_error=True)
        self.refrescar()

    def limpiar_campos(self) -> None:
        self.id_editando = None
        self.txt_nombre.value = ""
        self.txt_precio.value = ""
        self.txt_stock.value = ""

    def limpiar(self, e) -> None:
        self.limpiar_campos()
        self.mostrar_mensaje("")
        self.page.update()

    def refrescar(self) -> None:
        self.cargar_tabla()
        self.page.update()
