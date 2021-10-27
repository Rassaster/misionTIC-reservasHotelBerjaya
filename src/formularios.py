from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField, DateField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo

class Login(FlaskForm):
	email = EmailField('E-mail *', validators = [InputRequired(message = 'El email es requerido')])
	clave = PasswordField('Contraseña *', validators = [InputRequired(message = 'La clave es requerida')])
	logIn = SubmitField('Ingresar')

class Registro(FlaskForm):    
	nombre = TextField('Nombre')
	apellido = TextField('Apellido')
	tipoDoc = SelectField(u'Tipo de documento', choices=[('Cedula'), ('Pasaporte'), ('Cedula de extranjeria')])
	documento = TextField('Documento')
	guardar = SubmitField('Guardar')
	actuali = SubmitField('Actualizar')

class NuevoUsr(FlaskForm):    
	email = EmailField('E-Mail', validators = [InputRequired(message='El email es requerido')])
	passn = PasswordField('Contraseña', validators = [InputRequired(message='La clave es requerida')])
	passv = PasswordField('Confirmar Contraseña', validators = [InputRequired(message='La verificación de clave es requerida'), EqualTo(passn,'La nueva clave y su verificación no corresponden')])
	enviar = SubmitField('Ingresar')

class HabitacionesForm(FlaskForm):
	numeroHab = TextField('Numero de Habitacion')
	caract = TextField('Caracteristicas')
	# caract = SelectField(u'Caracteristicas', choices=[('Familiar'), ('Deluxe'), ('Emperatriz')])
	precio = TextField('Precio')
	guardar = SubmitField('Guardar')
	actuali = SubmitField('Actualizar')

class ReservasForm(FlaskForm):
	documento = TextField('Numero documento')
	habitacion = TextField('Numero habitacion')
	fechaIn = TextField('Fecha entrada')
	fechaOut = TextField('Fecha salida')
	guardar = SubmitField('Guardar')

class ComentariosForm(FlaskForm):
	documento = TextField('Numero documento')
	habitacion = TextField('Numero habitacion')
	calificacion = TextField('Calificacion')
	comentario = TextField('Comentario')
	guardar = SubmitField('Guardar')