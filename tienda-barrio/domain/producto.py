from typing import Optional


class Producto:
    """Representa un producto que se vende en la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int, id: Optional[int] = None) -> None:
        self.__id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    # ---------- Propiedades ----------
    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto es obligatorio")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        self.__precio = float(valor)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("El stock no puede ser negativo")
        self.__stock = int(valor)

    # ---------- Método de fábrica ----------
    @classmethod
    def desde_tupla(cls, fila: tuple) -> "Producto":
        """Crea un Producto a partir de una fila: (id, nombre, precio, stock)."""
        return cls(id=fila[0], nombre=fila[1], precio=fila[2], stock=fila[3])

    # ---------- Métodos mágicos ----------
    def __str__(self) -> str:
        return f"{self.__nombre} (${self.__precio:,.0f})"

    def __repr__(self) -> str:
        return f"Producto(id={self.__id}, nombre='{self.__nombre}', precio={self.__precio}, stock={self.__stock})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Producto):
            return False
        return self.__id == otro.id
