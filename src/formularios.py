from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo

class Login(FlaskForm):
	email = EmailField('E-mail *', validators = [InputRequired(message = 'El email es requerido')])
	clave = PasswordField('Contraseña *', validators = [InputRequired(message = 'La clave es requerida')])
	logIn = SubmitField('Ingresar')
	signUp = SubmitField('Registarse')

class Registro(FlaskForm):    
	nombre = TextField('Nombre ')
	apellido = TextField('Apellido ')
	documento = TextField('Documento ')
	fechaIn = DateField('Fecha de Entrada ')
	logIn = SubmitField('Ingresar')
	signUp = SubmitField('Registrarse')

class NuevoUsr(FlaskForm):    
	email = EmailField('E-Mail *', validators = [InputRequired(message='El email es requerido')])
	passn = PasswordField('Contraseña *', validators = [InputRequired(message='La clave es requerida')])
	passv = PasswordField('Verifique *', validators = [InputRequired(message='La verificación de clave es requerida'), EqualTo(passn,'La nueva clave y su verificación no corresponden')])
	enviar = SubmitField('Ingresar')
