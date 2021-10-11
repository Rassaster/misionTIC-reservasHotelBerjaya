from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

class Login(FlaskForm):
    userId = TextField('Usuario *', validators = [InputRequired(message = 'El usuario es requerido')])
    clave = PasswordField('Contraseña *', validators = [InputRequired(message = 'La clave es requerida')])
    enviar = SubmitField('Entrar')   