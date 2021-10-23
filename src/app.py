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
        return render_template('login.html', form=frm, titulo='login')
    else:
        if frm.signUp.data:  
            return redirect('/nuevoUsr/')            
        elif frm.logIn.data:  
            ema = escape(frm.email.data.strip())
            cla = escape(frm.clave.data.strip())
            sql = f'SELECT usuario, contrasena FROM fullTable WHERE usuario="{ema}"'
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
    return render_template('login.html', form=frm, titulo='login')

@app.route('/nuevoUsr/', methods = ['GET', 'POST'])
def nuevoUsr():
    frm = NuevoUsr()
    if request.method == 'GET':
        return render_template('nuevoUsr.html', form=frm, titulo='Registro de usuarios')
    else:
        email = escape(request.form['email'])
        clave1 = escape(request.form['passn'])
        clave2 = escape(request.form['passv'])
        # if email == None or len(email) == 0 or not email_valido(email):
        if email == None or len(email) == 0:
            flash('ERROR: Debe suministrar un email válido')
        elif clave1 == None or len(clave1) == 0 or not pass_valido(clave1):
            flash('ERROR: Debe suministrar una clave válida')
        elif clave2 == None or len(clave2) == 0 or not pass_valido(clave2):
            flash('ERROR: Debe suministrar una verificación de clave válida')
        elif clave1 != clave2:
            flash('ERROR: La clave y la verificación no coinciden')
        else:
            sql = f"INSERT INTO fullTable (usuario, contrasena) VALUES (?, ?)"
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
        return render_template('nuevoUsr.html', form=frm, titulo='Registro de datos')

@app.route('/registro/')
def registro():
    frm = Registro()
    usr = session['usuario']
    flash('INFO: Sesion iniciada para: ' + usr)
    return render_template('registro.html',form=frm, titulo='Habitaciones')

@app.route('/habitaciones/')
def habitaciones():
    return render_template('habitaciones.html', titulo='Habitaciones')

@app.route('/contactanos/')
def contactanos():
    return render_template('contactanos.html')

@app.route('/instalaciones/')
def instalaciones():
    return render_template('instalaciones.html')

@app.route('/comentarios/')
def comentarios():
    habitacion = escape(request.args.get('habitacion', 'error'))
    sql = f"SELECT comen FROM fullTable WHERE caract='{habitacion}'"
    res = seleccion(sql)
    if len(res) == 0:
        dat = None
        msg = 'No existen registros'
    else:
        dat = res
        msg ='Se muestran los datos'

    return render_template('comentarios.html', data = dat, msg = msg)

if __name__ == '__main__':
    app.run()