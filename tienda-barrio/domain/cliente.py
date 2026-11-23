from typing import Optional


class Cliente:
    """Representa a un cliente de la tienda."""

    def __init__(self, nombre: str, telefono: str, direccion: str, id: Optional[int] = None) -> None:
        # Atributos privados (doble guion bajo) -> encapsulamiento
        self.__id = id
        self.nombre = nombre          # usa el setter para validar
        self.__telefono = telefono
        self.__direccion = direccion

    # ---------- Propiedades (getters y setters) ----------
    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente es obligatorio")
        self.__nombre = valor.strip()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @property
    def direccion(self) -> str:
        return self.__direccion

    # ---------- Método de fábrica ----------
    @classmethod
    def desde_tupla(cls, fila: tuple) -> "Cliente":
        """Crea un Cliente a partir de una fila de SQLite: (id, nombre, telefono, direccion)."""
        return cls(id=fila[0], nombre=fila[1], telefono=fila[2], direccion=fila[3])

    # ---------- Métodos mágicos ----------
    def __str__(self) -> str:
        return f"{self.__nombre} - Tel: {self.__telefono}"

    def __repr__(self) -> str:
        return f"Cliente(id={self.__id}, nombre='{self.__nombre}')"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cliente):
            return False
        return self.__id == otro.id
