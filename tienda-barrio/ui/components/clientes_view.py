import sqlite3

import flet as ft

from data.cliente_dao import ClienteDAO
from domain.cliente import Cliente


class ClientesView:
    """Pantalla de clientes: formulario + tabla con botones de editar y eliminar."""

    def __init__(self, page: ft.Page, dao: ClienteDAO) -> None:
        self.page = page
        self.dao = dao
        self.id_editando = None  # None = creando uno nuevo; un número = editando ese cliente

        # ---- Formulario ----
        self.txt_nombre = ft.TextField(label="Nombre", width=250)
        self.txt_telefono = ft.TextField(label="Teléfono", width=180)
        self.txt_direccion = ft.TextField(label="Dirección", width=250)
        self.btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar)
        self.btn_limpiar = ft.OutlinedButton("Limpiar", on_click=self.limpiar)
        self.mensaje = ft.Text("")
        self.lbl_total = ft.Text("")

        # ---- Tabla ----
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
        )

    def construir(self) -> ft.Control:
        """Devuelve todo el contenido de la pantalla."""
        self.cargar_tabla()
        return ft.Column(
            [
                ft.Text("Clientes", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.txt_nombre, self.txt_telefono, self.txt_direccion], wrap=True),
                ft.Row([self.btn_guardar, self.btn_limpiar]),
                self.mensaje,
                self.lbl_total,
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def cargar_tabla(self) -> None:
        """Lee los clientes de la BD y llena la tabla."""
        self.lbl_total.value = f"Total de clientes: {len(self.dao)}"   # usa __len__ del DAO
        self.tabla.rows.clear()
        for cliente in self.dao.listar():
            self.tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(cliente.id))),
                    ft.DataCell(ft.Text(cliente.nombre)),
                    ft.DataCell(ft.Text(cliente.telefono)),
                    ft.DataCell(ft.Text(cliente.direccion)),
                    ft.DataCell(ft.Row([
                        # c=cliente guarda el cliente de ESTA fila para el botón
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE,
                                      on_click=lambda e, c=cliente: self.editar(c)),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                      on_click=lambda e, c=cliente: self.eliminar(c)),
                    ])),
                ])
            )

    def mostrar_mensaje(self, texto: str, es_error: bool = False) -> None:
        self.mensaje.value = texto
        self.mensaje.color = ft.Colors.RED if es_error else ft.Colors.GREEN

    def guardar(self, e) -> None:
        try:
            cliente = Cliente(
                nombre=self.txt_nombre.value,
                telefono=self.txt_telefono.value or "",
                direccion=self.txt_direccion.value or "",
                id=self.id_editando,
            )
            if self.id_editando is None:
                self.dao.crear(cliente)
                self.mostrar_mensaje("Cliente creado correctamente")
            else:
                self.dao.actualizar(cliente)
                self.mostrar_mensaje("Cliente actualizado correctamente")
            self.limpiar_campos()
            self.refrescar()
        except ValueError as error:  # errores de validación del modelo
            self.mostrar_mensaje(str(error), es_error=True)
            self.page.update()

    def editar(self, cliente: Cliente) -> None:
        """Pasa los datos de la fila al formulario."""
        self.id_editando = cliente.id
        self.txt_nombre.value = cliente.nombre
        self.txt_telefono.value = cliente.telefono
        self.txt_direccion.value = cliente.direccion
        self.mostrar_mensaje(f"Editando: {cliente}")
        self.page.update()

    def eliminar(self, cliente: Cliente) -> None:
        try:
            self.dao.eliminar(cliente.id)
            self.mostrar_mensaje(f"Cliente '{cliente.nombre}' eliminado")
        except sqlite3.IntegrityError:
            # La llave foránea no deja borrar un cliente que tiene ventas
            self.mostrar_mensaje("No se puede eliminar: el cliente tiene ventas registradas", es_error=True)
        self.refrescar()

    def limpiar_campos(self) -> None:
        self.id_editando = None
        self.txt_nombre.value = ""
        self.txt_telefono.value = ""
        self.txt_direccion.value = ""

    def limpiar(self, e) -> None:
        self.limpiar_campos()
        self.mostrar_mensaje("")
        self.page.update()

    def refrescar(self) -> None:
        """Recarga la tabla y redibuja la pantalla."""
        self.cargar_tabla()
        self.page.update()
