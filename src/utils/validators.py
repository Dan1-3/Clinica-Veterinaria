# Aquí se crearán funciones o clases auxiliares para validar datos, como correos electrónicos / nº de teléfono.

# El objetivo es centralizar las validaciones comunes que se usan en varios servicios
# Y asi cumplir con el principio de responsabilidad única (SRP)

import re

class EmailValidator:
    @staticmethod
    def validar(email: str) -> bool:
        if not email:
            return False
        # Patrón estándar para emails --> tiene que contener usuario, @ y dominio
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(patron, email))

class TelefonoValidator:
    @staticmethod
    def validar(telefono: str) -> bool:
        # Validamos que el teléfono tenga 9 dígitos y empiece por 6
        if not telefono:
            return False

        patron = r'^6\d{8}$'
        return bool(re.match(patron, telefono))