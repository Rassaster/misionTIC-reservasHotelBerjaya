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

    if request.method == 'GET':
        return render_template('login.html', form=frm, titulo='Login')
    elif frm.logIn.data:  
        ema = escape(frm.email.data.strip())
        cla = escape(frm.clave.data.strip())

        sql = f'SELECT usuario, contrasena FROM credenciales WHERE usuario="{ema}"'
        res = seleccion(sql)

        if len(res) == 0:
            flash('ERROR: Email o clave invalidas')
            return redirect('/login/')
        else:
            claveHash = res[0][1]
            if check_password_hash(claveHash, cla):
                session.clear()
                session['usuario'] = res[0][0]
                session['contrasena'] = res[0][1]
                return redirect('/registro/')
            else:
                flash('ERROR: Email o clave invalidas')
                return redirect('/login/')

    return render_template('login.html', form=frm, titulo='Login')

@app.route('/nuevoUsr/', methods = ['GET', 'POST'])
def nuevoUsr():
    frm = NuevoUsr()

    if request.method == 'GET':
        return render_template('nuevoUsr.html', form=frm, titulo='Nuevo usuario')
    else:
        email = escape(request.form['email'])
        clave1 = escape(request.form['passn'])
        clave2 = escape(request.form['passv'])

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
            res = accion(sql,(email, pwd))
            if res != 0:
                flash('INFO: Datos almacenados con exito')
                session.clear()
                session['usuario'] = email
                session['contrasena'] = pwd
                return redirect('/registro/')
            else:
                flash('ERROR: Por favor reintente')

        return render_template('nuevoUsr.html', form=frm, titulo='Nuevo usuario')

@app.route('/registro/', methods = ['GET', 'POST'])
def registro():
    frm = Registro()
    usr = session['usuario']

    if request.method == 'GET':
        print(f'INFO: Sesion iniciada para: {usr}')

        return render_template('registro.html',form=frm, titulo='Registro')
    elif frm.reserva.data:
        nom = escape(request.form['nombre'])
        ape = escape(request.form['apellido'])
        tipoDoc = escape(request.form['tipoDoc'])
        doc = escape(request.form['documento'])
        dateIn = escape(request.form['fechaIn'])
        dateOut = escape(request.form['fechaOut'])
        tipoHab = escape(request.form['tipoHab'])
        numHab = escape(request.form['numeroHab'])
    # if frm.reserva.data:
        sql1 = f"INSERT INTO usuarios (nombre, apellido, tipo_documento, numero_documento, usuario) VALUES (?, ?, ?, ?, ?)"
        res1 = accion(sql1,(nom, ape, tipoDoc, doc, usr))
        sql3 = f'SELECT _id FROM usuarios WHERE usuario="{usr}"'
        res3 = seleccion(sql3)
        sql2 = f"INSERT INTO registros (cliente_id, habitacion_id, fecha_ingreso, fecha_salida) VALUES (?, ?, ?, ?)"
        res2 = accion(sql2,(res3[0][0], '1', dateIn, dateOut))
        if res1 != 0 and res2 != 0:
            flash('INFO: Datos almacenados con exito')
            # return redirect('/registro/')
        else:
            flash('ERROR: Por favor reintente')

    # for msg in get_flashed_messages():
    #     print(f'flashed_messages: {msg}')

    return render_template('registro.html',form=frm, titulo='Registro')

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

    sql = f"SELECT nombre, apellido, comen, calific FROM fullTable WHERE caract='{habitacion}'"
    res = seleccion(sql)
    if len(res) == 0:
        dat = None
        msg = 'No existen registros'
    else:
        dat = res
        msg ='Se muestran los datos'
    
    contexto = {
        'data' : dat, 
        'qRes' : msg, 
        'titulo' : 'Comentarios'
    }

    return render_template('comentarios.html', **contexto)

if __name__ == '__main__':
    app.run()