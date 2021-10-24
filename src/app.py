from flask import Flask, render_template, request, flash, redirect, session
from flask.globals import session
from formularios import Login, Registro, NuevoUsr
from utils import pass_valido
from markupsafe import escape
import os
from werkzeug.security import check_password_hash, generate_password_hash
from db import accion, seleccion

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def home():
	return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
	frm = Login()

	if frm.logIn.data:  
		ema = escape(frm.email.data.strip())
		cla = escape(frm.clave.data.strip())

		try:
			sql = f"SELECT usuario, contrasena FROM credenciales WHERE usuario = '{ema}'"
			res = seleccion(sql)

			if len(res) != 0 and check_password_hash(res[0][1], cla):
				session.clear()
				session['usuario'] = res[0][0]
				session['contrasena'] = res[0][1]
				return redirect('/registro/')

			flash('ERROR: Email o clave invalidas')
			return redirect('/login/')

		except Exception as ex:
			print(ex)

	return render_template('login.html', form = frm, titulo = 'Login')

@app.route('/nuevoUsr/', methods = ['GET', 'POST'])
def nuevoUsr():
	frm = NuevoUsr()
	if request.method == 'POST':
		email = escape(request.form['email'])
		clave1 = escape(request.form['passn'])
		clave2 = escape(request.form['passv'])

		try:
			sql = f"SELECT COUNT(usuario) FROM credenciales WHERE usuario='{email}'"
			res = seleccion(sql)

			if res[0][0] > 0:
				flash('ERROR: Por favor use otro correo, el ingresado ya existe')
			elif email == None or len(email) == 0:
				flash('ERROR: Debe suministrar un email válido')
			elif clave1 == None or len(clave1) == 0 or not pass_valido(clave1):
				flash('ERROR: Debe suministrar una clave válida')
			elif clave2 == None or len(clave2) == 0 or not pass_valido(clave2):
				flash('ERROR: Debe suministrar una verificación de clave válida')
			elif clave1 != clave2:
				flash('ERROR: La clave y la verificación no coinciden')
			else:
				sql = f"INSERT INTO credenciales (usuario, contrasena) VALUES (?, ?)"
				pwd = generate_password_hash(clave1)
				print(f'TEST: email: {email}, pwd: {pwd}')
				res = accion(sql,(email, pwd))
				print(f'res: {res}')

				if res != 0:
					flash('INFO: Datos almacenados con exito')
					session.clear()
					session['usuario'] = email
					session['contrasena'] = pwd
					return redirect('/registro/')
				else:
					flash('ERROR: Por favor reintente')
		except Exception as ex:
			print(ex)

	return render_template('nuevoUsr.html', form = frm, titulo = 'Nuevo usuario')

@app.route('/registro/', methods = ['GET', 'POST'])
def registro():
	frm = Registro()
	usr = session['usuario']

	if request.method == 'POST':
		nom = str(escape(request.form['nombre']))
		ape = str(escape(request.form['apellido']))
		tipoDoc = str(escape(request.form['tipoDoc']))
		doc = int(escape(request.form['documento']))
		dateIn = str(escape(request.form['fechaIn']))
		dateOut = str(escape(request.form['fechaOut']))
		tipoHab = str(escape(request.form['tipoHab']))
		numHab = int(escape(request.form['numeroHab']))

		try:
			# type(usuario) is str
			# type(contrasena) is str
			# type(estado) is str
			# type(calific) is int
			# type(comen) is str
			# type(pago) is bool
			# type(rol) is str
			# precio solo se LEE

			# hay que validar que el numero de cc sea nuevo
			# de donde saco user pass?
			# https://getbootstrap.com/docs/5.0/forms/validation/ server side

			# creo que podria quitar la validacion aqui porque estoy casteando arriba y elevar una exepcion arriba seria mejor
			if isinstance(nom, str) and isinstance(ape, str) and isinstance(tipoDoc, str) and isinstance(doc, int) and isinstance(dateIn, str) and isinstance(dateOut, str) and isinstance(tipoHab, str) and isinstance(numHab, int):
				sql = f"INSERT INTO fullTable (nombre, apellido, tipo_doc, num_doc, fecha_in, fecha_sal, caract, num_hab) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
				res = accion(sql, (nom, ape, tipoDoc, doc, dateIn, dateOut, tipoHab, numHab))

				if res != 0:
					flash('INFO: Datos almacenados con exito')
					return redirect('/registro/')
				else:
					flash('ERROR: Por favor reintente')
			else:
				print('TYPES NOT MATCH')
		except Exception as ex:
			print(f'ex100: {ex}')

	print(f'INFO: Sesion iniciada para: {usr}')
	return render_template('registro.html', form = frm, titulo = 'Registro')

@app.route('/habitaciones/')
def habitaciones():
	habFam = seleccion(f"SELECT COUNT(comen) FROM fullTable WHERE caract = 'familiar' AND estado = 'disponible'")
	habDel = seleccion(f"SELECT COUNT(comen) FROM fullTable WHERE caract = 'deluxe' AND estado = 'disponible'")
	habPen = seleccion(f"SELECT COUNT(comen) FROM fullTable WHERE caract = 'penthouse' AND estado = 'disponible'")

	familiarOpen = habFam[0][0]
	deluxeOpen = habDel[0][0]
	penthouseOpen = habPen[0][0]

	contexto = {
		'familiarOpen' : familiarOpen,
		'deluxeOpen' : deluxeOpen,
		'penthouseOpen' : penthouseOpen,
		'titulo' : 'Habitaciones'
	}

	return render_template('habitaciones.html', **contexto)

@app.route('/contactanos/')
def contactanos():
	return render_template('contactanos.html', titulo='Contactanos')

@app.route('/instalaciones/')
def instalaciones():
	return render_template('instalaciones.html')

@app.route('/comentarios/')
def comentarios():
	habitacion = escape(request.args.get('habitacion', 'error'))

	try:
		sql = f"SELECT nombre, apellido, comen, calific FROM fullTable WHERE caract='{habitacion}'"
		res = seleccion(sql)
		if len(res) == 0:
			dat = None
			msg = 'No existen registros'
		else:
			dat = res
			msg = 'Se muestran los datos'
		
		contexto = {
			'data' : dat, 
			'qRes' : msg, 
			'titulo' : 'Comentarios'
		}
	except Exception as ex:
		print(ex)

	return render_template('comentarios.html', **contexto)

@app.route('/gracias/')
def gracias():
	return render_template('gracias.html', titulo='Gracias')

if __name__ == '__main__':
	app.run()