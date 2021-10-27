from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField, DateField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo

class Login(FlaskForm):
	email = EmailField('E-mail *', validators = [InputRequired(message = 'El email es requerido')])
	clave = PasswordField('Contraseña *', validators = [InputRequired(message = 'La clave es requerida')])
	logIn = SubmitField('Ingresar')

class Registro(FlaskForm):    
	nombre = TextField('Nombre ')
	apellido = TextField('Apellido ')
	tipoDoc = SelectField(u'Tipo de documento', choices=[('Cedula'), ('Pasaporte'), ('Cedula de extranjeria')])
	documento = TextField('Documento ')
	fechaIn = DateField('Fecha de Entrada ')
	fechaOut = DateField('Fecha de Salida ')
	tipoHab = SelectField(u'Tipo de Habitacion', choices=[('Familiar'), ('Deluxe'), ('Emperatriz')])
	numeroHab = TextField('Numero Habitacion ')
	precioHab = TextField('Precio Habitacion ')
	reserva = SubmitField('Ingresar')

class NuevoUsr(FlaskForm):    
	email = EmailField('E-Mail *', validators = [InputRequired(message='El email es requerido')])
	passn = PasswordField('Contraseña *', validators = [InputRequired(message='La clave es requerida')])
	passv = PasswordField('Verifique *', validators = [InputRequired(message='La verificación de clave es requerida'), EqualTo(passn,'La nueva clave y su verificación no corresponden')])
	enviar = SubmitField('Ingresar')
