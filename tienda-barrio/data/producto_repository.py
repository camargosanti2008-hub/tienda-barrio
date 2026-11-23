from typing import Optional

from data.database_manager import DatabaseManager
from domain.producto import Producto


class ProductoRepository:
    """Repository de productos: guarda y recupera objetos Producto de la base de datos."""

    def __init__(self, ruta_db: str) -> None:
        self._ruta_db = ruta_db

    def crear(self, producto: Producto) -> int:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (producto.nombre, producto.precio, producto.stock),
            )
            return cursor.lastrowid

    def listar(self) -> list[Producto]:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY nombre")
            filas = cursor.fetchall()
        return [Producto.desde_tupla(fila) for fila in filas]

    def buscar_por_id(self, id_producto: int) -> Optional[Producto]:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE id = ?", (id_producto,))
            fila = cursor.fetchone()
        return Producto.desde_tupla(fila) if fila else None

    def actualizar(self, producto: Producto) -> None:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute(
                "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
                (producto.nombre, producto.precio, producto.stock, producto.id),
            )

    def eliminar(self, id_producto: int) -> None:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))

    def __len__(self) -> int:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT COUNT(*) FROM productos")
            return cursor.fetchone()[0]
