from typing import Optional

from data.database_manager import DatabaseManager
from domain.cliente import Cliente


class ClienteDAO:
    """DAO = Data Access Object. Aquí van TODAS las consultas SQL de la tabla clientes.
    La interfaz nunca escribe SQL, solo llama a estos métodos."""

    def __init__(self, ruta_db: str) -> None:
        self._ruta_db = ruta_db

    def crear(self, cliente: Cliente) -> int:
        with DatabaseManager(self._ruta_db) as cursor:
            # Los "?" evitan la inyección SQL: los valores se envían aparte
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, direccion) VALUES (?, ?, ?)",
                (cliente.nombre, cliente.telefono, cliente.direccion),
            )
            return cursor.lastrowid

    def listar(self) -> list[Cliente]:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT id, nombre, telefono, direccion FROM clientes ORDER BY nombre")
            filas = cursor.fetchall()
        return [Cliente.desde_tupla(fila) for fila in filas]

    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT id, nombre, telefono, direccion FROM clientes WHERE id = ?", (id_cliente,))
            fila = cursor.fetchone()
        return Cliente.desde_tupla(fila) if fila else None

    def actualizar(self, cliente: Cliente) -> None:
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute(
                "UPDATE clientes SET nombre = ?, telefono = ?, direccion = ? WHERE id = ?",
                (cliente.nombre, cliente.telefono, cliente.direccion, cliente.id),
            )

    def eliminar(self, id_cliente: int) -> None:
        # Si el cliente tiene ventas, SQLite lanza IntegrityError por la llave foránea
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))

    def __len__(self) -> int:
        """Permite hacer len(cliente_dao) para saber cuántos clientes hay."""
        with DatabaseManager(self._ruta_db) as cursor:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            return cursor.fetchone()[0]
