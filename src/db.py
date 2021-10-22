import sqlite3
DB_URL = 'bd/test.db'

def accion(query) -> int:
# def accion(email, clave1) -> int:
	""" Se encarga de ejecutar una consulta de accion (INSERT, DELETE, UPDATE) """
	try:
		print(f'query:{query}')
		# print(f'email:{email}, clave1:{clave1}')
		with sqlite3.connect(DB_URL) as con:
			print("with")
			cur = con.cursor()
			sal = cur.execute(query).rowcount
			# sal = (cur.execute("INSERT INTO credenciales(usuario, contrasena) VALUES (?, ?)", (email, clave1))).rowcount
			# sal = (cur.execute("INSERT INTO credenciales(usuario, pass) VALUES (?, ?)", (email, clave1))).rowcount
			print(f'sal:{sal}')
		if sal != 0:
			print('check')
			con.commit()
	except Exception as ex:
		print(f'fail: {ex}')
		sal = 0
	return sal

def seleccion(query) -> list:
	""" Se encarga de ejecutar una consulta de selección (SELECT) """
	try:
		with sqlite3.connect(DB_URL) as con:
			cur = con.cursor()
			sal = cur.execute(query).fetchall()
	except Exception as ex:
		sal = []
	return sal