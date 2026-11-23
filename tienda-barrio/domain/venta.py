from typing import Optional


class Venta:
    """Representa una venta: un cliente compra cierta cantidad de un producto."""

    def __init__(self, cliente_id: int, producto_id: int, cantidad: int,
                 total: float = 0.0, fecha: str = "", id: Optional[int] = None,
                 cliente_nombre: str = "", producto_nombre: str = "") -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        self.__id = id
        self.__cliente_id = cliente_id
        self.__producto_id = producto_id
        self.__cantidad = cantidad
        self.__total = total
        self.__fecha = fecha
        # Estos dos solo sirven para mostrar los nombres en la tabla
        self.__cliente_nombre = cliente_nombre
        self.__producto_nombre = producto_nombre

    # ---------- Propiedades (solo lectura) ----------
    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def cliente_id(self) -> int:
        return self.__cliente_id

    @property
    def producto_id(self) -> int:
        return self.__producto_id

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def total(self) -> float:
        return self.__total

    @property
    def fecha(self) -> str:
        return self.__fecha

    @property
    def cliente_nombre(self) -> str:
        return self.__cliente_nombre

    @property
    def producto_nombre(self) -> str:
        return self.__producto_nombre

    # ---------- Método de fábrica ----------
    @classmethod
    def desde_tupla(cls, fila: tuple) -> "Venta":
        """Crea una Venta a partir de la fila del JOIN:
        (id, cliente_id, producto_id, cantidad, total, fecha, cliente_nombre, producto_nombre)."""
        return cls(id=fila[0], cliente_id=fila[1], producto_id=fila[2], cantidad=fila[3],
                   total=fila[4], fecha=fila[5], cliente_nombre=fila[6], producto_nombre=fila[7])

    # ---------- Métodos mágicos ----------
    def __str__(self) -> str:
        return f"Venta #{self.__id}: {self.__cantidad} x {self.__producto_nombre} = ${self.__total:,.0f}"

    def __repr__(self) -> str:
        return f"Venta(id={self.__id}, cliente_id={self.__cliente_id}, producto_id={self.__producto_id}, cantidad={self.__cantidad})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Venta):
            return False
        return self.__id == otro.id
