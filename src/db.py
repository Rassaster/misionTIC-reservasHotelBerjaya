import sqlite3
DB_URL = 'bd/test2.db'

def accion(query) -> int:
# def accion(email, clave1) -> int:
	""" Se encarga de ejecutar una consulta de accion (INSERT, DELETE, UPDATE) """
	try:
		# print(f'email:{email}, clave1:{clave1}')
		with sqlite3.connect(DB_URL) as con:
			print(f'query:{query}')
			cur = con.cursor()
			sal = cur.execute(query).rowcount
			# sal = (cur.execute("INSERT INTO credenciales(usuario, contrasena) VALUES (?, ?)", (email, clave1))).rowcount
			# sal = (cur.execute("INSERT INTO credenciales(usuario, pass) VALUES (?, ?)", (email, clave1))).rowcount
		if sal != 0:
			print(f'sal:{sal}')
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