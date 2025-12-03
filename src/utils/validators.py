# Aquí se crearán funciones o clases auxiliares para validar datos,
# como correos electrónicos o números de teléfono.

import re

class EmailValidator:
    @staticmethod
    def validar(email: str) -> bool:
        if not email:
            return False
        # Patrón estándar para emails
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(patron, email))

class TelefonoValidator:
    @staticmethod
    def validar(telefono: str) -> bool:
        """
        Valida si el teléfono tiene 9 dígitos y EMPIEZA POR 6.
        """
        if not telefono:
            return False
        # Patrón: Empieza por 6, seguido de 8 dígitos más
        patron = r'^6\d{8}$'
        return bool(re.match(patron, telefono))