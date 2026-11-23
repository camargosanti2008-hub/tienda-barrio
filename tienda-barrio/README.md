# Tienda de Barrio La Esquina – Sistema de Gestión

Proyecto final de **Programación II** (Universidad de Cundinamarca).
Aplicación de escritorio hecha con **Flet** y **SQLite** para registrar clientes, productos (inventario) y ventas de una tienda de barrio.

## Requisitos
- Python 3.10 o superior
- Flet: `pip install flet`

## Cómo ejecutar
```bash
python main.py
```
La base de datos `tienda.db` se crea sola la primera vez.

## Estructura
```
tienda_barrio/
├── main.py                  # Punto de entrada
├── README.md
├── informe_final.pdf
├── data/                    # Capa de persistencia
│   ├── database_manager.py  # Conexión, commit/rollback, PRAGMA foreign_keys
│   ├── cliente_dao.py       # SQL de clientes
│   ├── producto_repository.py
│   └── venta_dao.py
├── domain/                  # Capa de negocio (modelos)
│   ├── cliente.py
│   ├── producto.py
│   └── venta.py
└── ui/                      # Capa de interfaz Flet
    ├── app_view.py          # Ventana principal y menú
    └── components/
        ├── clientes_view.py
        ├── productos_view.py
        └── ventas_view.py
```

## Funcionalidades
- CRUD completo de clientes, productos y ventas.
- Al registrar una venta se descuenta el stock; al eliminarla o editarla se ajusta.
- No deja vender más unidades de las que hay (se hace rollback).
- No deja eliminar un cliente o producto que tenga ventas (llave foránea).
