from datetime import datetime

from data.database_manager import DatabaseManager
from domain.venta import Venta


class VentaDAO:
    """DAO de ventas. Al vender también descuenta el stock del producto.
    Todo ocurre dentro de UNA transacción: si algo falla, se hace rollback y no se guarda nada."""

    def __init__(self, ruta_db: str) -> None:
        self._ruta_db = ruta_db

    def _descontar_stock(self, cursor, producto_id: int, cantidad: int) -> float:
        """Revisa el stock, lo descuenta y devuelve el precio del producto."""
        cursor.execute("SELECT precio, stock FROM productos WHERE id = ?", (producto_id,))
        fila = cursor.fetchone()
        if fila is None:
            raise ValueError("El producto no existe")
        precio, stock = fila
        if cantidad > stock:
            raise ValueError(f"Stock insuficiente: solo hay {stock} unidades")
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
        return precio

    def _devolver_stock(self, cursor, venta_id: int) -> None:
        """Devuelve al inventario las unidades de una venta existente."""
        cursor.execute("SELECT producto_id, cantidad FROM ventas WHERE id = ?", (venta_id,))
        fila = cursor.fetchone()
        if fila is None:
            raise ValueError("La venta no existe")
        producto_id, cantidad = fila
        cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, producto_id))

    def crear(self, venta: Venta) -> int:
        with DatabaseManager(self._ruta_db) as cursor:
            precio = self._descontar_stock(cursor, venta.producto_id, venta.cantidad)
            total = precio * venta.cantidad
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO ventas (cliente_id, producto_id, cantidad, total, fecha) VALUES (?, ?, ?, ?, ?)",
                (venta.cliente_id, venta.producto_id, venta.cantidad, total, fecha),
            )
            return cursor.lastrowid

    def listar(self) -> list[Venta]:
        with DatabaseManager(self._ruta_db) as cursor:
            # JOIN para traer también el nombre del cliente y del producto
            cursor.execute("""
                SELECT v.id, v.cliente_id, v.producto_id, v.cantidad, v.total, v.fecha,
                       c.nombre, p.nombre
                FROM ventas v
                JOIN clientes c  ON v.cliente_id = c.id
                JOIN productos p ON v.producto_id = p.id
                ORDER BY v.id DESC
            """)
            filas = cursor.fetchall()
        return [Venta.desde_tupla(fila) for fila in filas]

    def actualizar(self, venta: Venta) -> None:
        with DatabaseManager(self._ruta_db) as cursor:
            self._devolver_stock(cursor, venta.id)                                    # 1. devolver lo de antes
            precio = self._descontar_stock(cursor, venta.producto_id, venta.cantidad)  # 2. descontar lo nuevo
            total = precio * venta.cantidad
            cursor.execute(
                "UPDATE ventas SET cliente_id = ?, producto_id = ?, cantidad = ?, total = ? WHERE id = ?",
                (venta.cliente_id, venta.producto_id, venta.cantidad, total, venta.id),
            )

    def eliminar(self, id_venta: int) -> None:
        with DatabaseManager(self._ruta_db) as cursor:
            self._devolver_stock(cursor, id_venta)
            cursor.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))

    def __len__(self) -> int:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT COUNT(*) FROM ventas")
            return cursor.fetchone()[0]
