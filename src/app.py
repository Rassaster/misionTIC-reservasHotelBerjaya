from flask import Flask, render_template, request
from formularios import Login, Registro
from markupsafe import escape
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def home():
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method=='GET':
        frm = Login()
        return render_template('login.html', form=frm, titulo='login')
    else:
        usr = escape(request.form['userId'])
        cla = escape(request.form['clave'])
        sal = ''
        if len(usr.strip()) < 5 or len(usr.strip()) > 40:
            sal += 'User between 5 and 40 chars'
        if len(cla.strip()) < 5 or len(cla.strip()) > 40:
            sal += 'Password between 5 and 40 chars'
        if sal == '':
            sal = 'Data validated'
        sal += '<a href="/">Back home</a>'
        return sal

@app.route('/registro/', methods=['GET','POST'])
def registro():
    if request.method=='GET':
        # Se debe crear una instancia del formulario
        frm = Registro()
        return render_template('registro.html',form=frm,titulo='Registro de usuarios')
    # else:
    #     # recuperar los datos del formulario
    #     nom = escape(request.form["nombre"]) # Dificultar la inyección de código
    #     ape = escape(request.form["apellido"]) # Dificultar la inyección de código
    #     # Validar los datos del lado del servidor
    #     sal = ''
    #     if len(nom.strip())<1:
    #         sal += 'Los nombres son requeridos' 
    #     if len(ape.strip())<1:
    #         sal += 'Los apellidos son requeridos' 
    #     if sal=='':
    #         sal = 'Los datos son válidos, deberíamos consultar a la BD'
    #     sal += '<a href="/">Volver al inicio</a>'
    #     return sal

# @app.route('/habitaciones/')
# def habitaciones():
#     return render_template('habitaciones.html', form=frm, titulo='Habitaciones')

if __name__ == '__main__':
    app.run()