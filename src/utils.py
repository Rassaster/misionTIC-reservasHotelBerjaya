import re
# from validate_email import validate_email

# def email_valido(email):
#     return validate_email(email)
    
# def login_valido(login):
#     return re.search('^[a-zA-Z0-9_\-.]{5,40}$',login)

def pass_valido(clave):
    # return True
    # La contraseña debe tener al entre 6 y 14 caracteres, al menos un dígito, al menos una minúscula y al menos una mayúscula.NO puede tener otros símbolos.
    return re.search('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{6,14}$', clave)