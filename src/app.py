from flask import Flask, render_template, request, flash, redirect, session
from flask.globals import session
from formularios import Login, Registro, NuevoUsr, HabitacionesForm
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

		try:
			if isinstance(nom, str) and isinstance(ape, str) and isinstance(tipoDoc, str) and isinstance(doc, int):
				print('555try')
				sql = f"INSERT INTO usuarios (usuario, nombre, apellido, tipo_documento, numero_documento) VALUES (?, ?, ?, ?, ?)"
				res = accion(sql, (usr, nom, ape, tipoDoc, doc))

				print('555if')
				if res != 0:
					print('flash')
					flash('INFO: Datos almacenados con exito')
					return redirect('/registro/')
				else:
					flash('ERROR: No se pudieron guardar los datos')
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
	return render_template('contactanos.html', titulo = 'Contactanos')

@app.route('/administrar/')
def administrar():
	return render_template('administrar.html', titulo = 'Admin')

@app.route('/adminHabitaciones/', methods=['GET', 'POST'])
def adminHabitaciones():
	frm = HabitacionesForm()

	if request.method == 'POST':
		try:
			numHab = int(escape(request.form['numeroHab']))
			carac = escape(request.form['caract'])
			precio = int(escape(request.form['precio']))
			guardar = request.form.get('guardar', False)
			actuali = request.form.get('actuali', False)
			
			habs = seleccion(f"SELECT numero_habitacion FROM habitaciones WHERE numero_habitacion = {numHab}")

			if len(str(numHab)) != 0 and len(carac) != 0 and len(str(precio)) != 0:
				if len(habs) == 0:
					if guardar:
						insHab = "INSERT INTO habitaciones (numero_habitacion, precio, caracteristicas) VALUES (?, ?, ?)"
						resInsHab = accion(insHab, (numHab, carac, precio))
						if resInsHab > 0:
							flash('Se guardaron los datos de la habitacion con exito')
					else:
						flash('La habitacion no existe, intente guardar')
				
				else:
					if actuali:
						resUpdHab = accion("UPDATE habitaciones SET precio = ?, caracteristicas = ? WHERE numero_habitacion = ?", (precio, carac, numHab))
						if resUpdHab == 0:
							flash('No se pudo actualizar la informacion')
						else:
							flash('La informacion para la habitacion ha sido actualizada')
					else:
						flash('La habitacion ya existe, intente actualizar')

			else:
				flash('Por favor llene todos los campos')

		except ValueError as ve:
			flash(f'La informacion ingresada no es valida o esta incompleta')

	return render_template('adminHabitaciones.html', form = frm, titulo = 'Admin')

@app.route('/comentarios/')
def comentarios():
	habitacion = escape(request.args.get('habitacion', 'error'))

	try:
		sql = f"SELECT nombre, apellido, comen, calific FROM fullTable WHERE caract = '{habitacion}'"
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
	return render_template('gracias.html', titulo = 'Gracias')

if __name__ == '__main__':
	app.run()