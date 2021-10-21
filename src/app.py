from flask import Flask, render_template, request, flash
from formularios import Login, Registro
from utils import pass_valido
from markupsafe import escape
import os
from werkzeug.security import check_password_hash, generate_password_hash
from db import accion

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
    # else:
    #     usr = escape(frm.userId.data.strip())
    #     cla = escape(frm.clave.data.strip())
        
    #     # sql = f'SELECT '
    #     sal = ''
    #     if len(usr.strip()) < 5 or len(usr.strip()) > 40:
    #         sal += 'User between 5 and 40 chars'
    #     if len(cla.strip()) < 5 or len(cla.strip()) > 40:
    #         sal += 'Password between 5 and 40 chars'
    #     if sal == '':
    #         sal = 'Data validated'
    #     sal += '<a href="/">Back home</a>'
    #     return sal

@app.route('/registro/', methods = ['GET', 'POST'])
def registro():
    frm = Registro()
    if request.method=='GET':
        return render_template('registro.html', form=frm, titulo='Registro de usuarios')
    else:
        email = escape(request.form['email'])
        clave1 = escape(request.form['passn'])
        clave2 = escape(request.form['passv'])
        swerror = False
        # if email == None or len(email) == 0 or not email_valido(email):
        if email == None or len(email) == 0:
            flash('ERROR: Debe suministrar un email válido')
            swerror = True
        if clave1 == None or len(clave1) == 0 or not pass_valido(clave1):
            flash('ERROR: Debe suministrar una clave válida')
            swerror = True
        if clave2 == None or len(clave2) == 0 or not pass_valido(clave2):
            flash('ERROR: Debe suministrar una verificación de clave válida')
            swerror = True
        if clave1 != clave2:
            flash('ERROR: La clave y la verificación no coinciden')
            swerror = True
        print(swerror)
        if not swerror:           
            sql = "INSERT INTO credenciales(usuario, contrasena) VALUES (?, ?)"
            pwd = generate_password_hash(clave1)
            res = accion(sql,(email, pwd))
            print(res)
            if res!=0:
                flash('INFO: Datos almacenados con exito')
            else:
                flash('ERROR: Por favor reintente')
        return render_template('registro.html', form=frm, titulo='Registro de datos')

@app.route('/habitaciones/')
def habitaciones():
    return render_template('habitaciones.html', titulo='Habitaciones')

@app.route('/contactanos/')
def contactanos():
    return render_template('contactanos.html')

@app.route('/instalaciones/')
def instalaciones():
    return render_template('instalaciones.html')

if __name__ == '__main__':
    app.run()