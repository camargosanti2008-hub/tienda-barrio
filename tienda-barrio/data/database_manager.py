import sqlite3


class DatabaseManager:
    """Maneja la conexión a SQLite usando 'with'.

    Uso:
        with DatabaseManager("tienda.db") as cursor:
            cursor.execute("SELECT ...")

    - Al entrar (__enter__) abre la conexión y activa las llaves foráneas.
    - Al salir (__exit__) hace commit si todo salió bien, o rollback si hubo un error,
      y siempre cierra la conexión.
    """

    def __init__(self, ruta_db: str = "tienda.db") -> None:
        self._ruta_db = ruta_db
        self._conexion = None

    def __enter__(self) -> sqlite3.Cursor:
        self._conexion = sqlite3.connect(self._ruta_db)
        # Integridad referencial: SQLite la trae apagada por defecto
        self._conexion.execute("PRAGMA foreign_keys = ON;")
        return self._conexion.cursor()

    def __exit__(self, tipo_error, valor_error, traza) -> bool:
        if tipo_error is None:
            self._conexion.commit()      # todo bien -> guardar cambios
        else:
            self._conexion.rollback()    # hubo error -> deshacer cambios
        self._conexion.close()
        return False  # False = el error (si hubo) se sigue propagando para mostrarlo en pantalla

    @staticmethod
    def crear_tablas(ruta_db: str) -> None:
        """Crea las 3 tablas si todavía no existen."""
        with DatabaseManager(ruta_db) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre    TEXT NOT NULL,
                    telefono  TEXT,
                    direccion TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    stock  INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id  INTEGER NOT NULL,
                    producto_id INTEGER NOT NULL,
                    cantidad    INTEGER NOT NULL,
                    total       REAL NOT NULL,
                    fecha       TEXT NOT NULL,
                    FOREIGN KEY (cliente_id)  REFERENCES clientes(id),
                    FOREIGN KEY (producto_id) REFERENCES productos(id)
                )
            """)
