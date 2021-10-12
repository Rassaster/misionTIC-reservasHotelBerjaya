from flask import Flask, render_template, request
from formularios import Login
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

if __name__ == '__main__':
    app.run(port=8000)