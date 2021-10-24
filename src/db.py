import sqlite3
DB_URL = 'bd/test2.db'

def accion(sql, data) -> int:
	""" Se encarga de ejecutar una consulta de accion (INSERT, DELETE, UPDATE) """
	try:
		with sqlite3.connect(DB_URL) as con:
			cur = con.cursor()
			sal = cur.execute(sql, data).rowcount
			print(f'accion: {sal}')
			if sal != 0:
				con.commit()
	except Exception as ex:
		print(f'Exception: {ex}')
		sal = 0
	return sal

def seleccion(query) -> list:
	""" Se encarga de ejecutar una consulta de selección (SELECT) """
	try:
		with sqlite3.connect(DB_URL) as con:
			cur = con.cursor()
			sal = cur.execute(query).fetchall()
			print(f'seleccion: {sal}')
	except Exception as ex:
		print(f'Exception: {ex}')
		sal = []
	return sal