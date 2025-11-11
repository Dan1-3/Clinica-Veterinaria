# Aquí se establecerá la conexión con la base de datos (SQLite).
# Más adelante se añadirá el código para crear y gestionar la sesión de conexión.

class DatabaseConnection:
    """Responsable de la conexión y sesión con la base de datos."""
    def _init_(self, url: str):
        pass

    def get_session(self):
        return self.Session()
