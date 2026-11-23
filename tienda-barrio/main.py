import os

import flet as ft

from data.database_manager import DatabaseManager
from ui.app_view import AppView

# La base de datos se guarda en la misma carpeta de este archivo
RUTA_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tienda.db")


def main(page: ft.Page) -> None:
    DatabaseManager.crear_tablas(RUTA_DB)  # crea las tablas la primera vez
    AppView(page, RUTA_DB)                 # arma la interfaz


if __name__ == "__main__":
    ft.app(target=main)
