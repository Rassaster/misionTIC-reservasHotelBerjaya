import re

def pass_valido(clave):
    # La contraseña debe tener al entre 6 y 14 caracteres, al menos un dígito, al menos una minúscula y al menos una mayúscula.NO puede tener otros símbolos.
    return re.search('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{6,14}$', clave)