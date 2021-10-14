from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo

class Login(FlaskForm):
    userId = TextField('Usuario *', validators = [InputRequired(message = 'El usuario es requerido')])
    clave = PasswordField('Contraseña *', validators = [InputRequired(message = 'La clave es requerida')])
    enviar = SubmitField('Entrar')   

class Registro(FlaskForm):    
    email = EmailField('E-Mail *', validators = [InputRequired(message='El email es requerido')])
    passn = PasswordField('Password *', validators = [InputRequired(message='La clave es requerida')])
    passv = PasswordField('Verifique *', validators = [InputRequired(message='La verificación de clave es requerida'), EqualTo(passn,'La nueva clave y su verificación no corresponden')])
    enviar = SubmitField('Ingresar')