import re

def es_correo_corporativo(email):
    # Ajusta este patrón según el dominio de correo corporativo de tu empresa
    patron = r'^[\w\.-]+@gmail\.com$'
    return re.match(patron, email) is not None
