#! /usr/bin/python
import psycopg2, sys, os, random
from random import randint
import django
from faker import Faker
from django.db import IntegrityError

def random_dni():
    return (lambda x: '%s%s' % (x, "TRWAGMYFPDXBNJZSQVHLCKE"[x % 23]))(random.randint(10000000, 99999999))

def destroy():
		c.execute(""" DELETE from "tfg_encuesta" """)
		c.execute(""" DELETE from "tfg_curso_alumno" """)
		c.execute(""" DELETE from "Alumno_curs" """)
		c.execute(""" DELETE from "Nota" """)
		c.execute(""" DELETE from "Completado" """)
		c.execute(""" DELETE from "Alumno" """)
		c.execute(""" DELETE from "Curso" """)
		c.execute(""" DELETE from "Profesor" """)
		c.execute(""" DELETE from "tfg_curso_alumno" """)
		c.execute(""" DELETE from "NivelConPassword" """)
		c.execute(""" DELETE from "NivelSinPassword" """)
		c.execute(""" DELETE from "Nivel" """)
		c.execute(""" DELETE from "tfg_practica" """)
		conn.commit()

fake = Faker('es_ES')


cursos = 100
add_cursos = True
alumnos = 100
Profesores = 50
practicas = 100
niveles = 200
fin = True
add_alumno = True
add_Curso_alumno = True
add_profesor = True
add_encuesta = True
add_practica = True
add_nivel = True
add_completado = True
add_nota = True
add_con_passwd = True
add_sin_passwd = True
delete_everything = True

if __name__ == '__main__':
	try:
		dades_str = "dbname='v' user='dabd_victor' host='localhost' password='dabd_victor'"
		conn = psycopg2.connect(dades_str)
		c = conn.cursor()
		print("conexio amb la base de dades correcte")
	except:
		print("conexio amb la base de dades erronia")
		sys.exit(1)

	print("Bienvenido al script de DABD de Victor selecciona una opcion ")
	operacion = int(input("Introducir datos (opcion 0) ||  Eliminar toda la base de datos (opcion 1) : "))
	if operacion == 1:
		destroy()
		print("cerrando conexion")
		c.close()
		conn.close()
	else:

		alumnos = int(input("Introdueix quants alumnes vols crear "))
		Profesores = int(input("Introdueix quants professors vols crear "))
		niveles  = int(input("Introdueix quants nivells vols crear "))
			
		if delete_everything:
			c.execute(""" DELETE from "tfg_encuesta" """)
			c.execute(""" DELETE from "tfg_curso_alumno" """)
			c.execute(""" DELETE from "Alumno_curs" """)
			c.execute(""" DELETE from "Nota" """)
			c.execute(""" DELETE from "Completado" """)
			c.execute(""" DELETE from "Alumno" """)
			c.execute(""" DELETE from "Curso" """)
			c.execute(""" DELETE from "Profesor" """)
			c.execute(""" DELETE from "tfg_curso_alumno" """)
			c.execute(""" DELETE from "NivelConPassword" """)
			c.execute(""" DELETE from "NivelSinPassword" """)
			c.execute(""" DELETE from "Nivel" """)
			c.execute(""" DELETE from "tfg_practica" """)
			c.execute(""" DROP INDEX "al" """)
			conn.commit()

			#taula Curso
		if add_cursos:
			Cursos_uni = ['DABD2019', 'DABD2020', 'DABD2018', 'DABD2017', 'DABD2016', 'DABD2015','DABD2014','DABD2013','DABD2012',
			'DABD2011','DABD2010','DABD2009','DABD2008','DABD2007','DABD2006','DABD2005','DABD2004','DABD2003','DABD2002','DABD2001','DABD2000',
			'DABD1999','DABD1998','DABD1997','DABD1996','DABD1995','DABD1994','DABD1993','DABD1992','DABD1991','DABD1990']
			for i in range(cursos):
				#info = [(random.choice(Cursos_uni)),fake.date_between(start_date="-20y", end_date="today"),"2019-06-30"]
				info = [(random.choice(Cursos_uni)),fake.date_between(start_date="-20y", end_date="-1y"),fake.date_between(start_date="-1y", end_date="+1y")]
				if True:
					r = c.execute("""SELECT count(*) from "Curso" where "Asignatura" =  '%s';""" %(info[0]))
					result=c.fetchone()
				if (result[0] == 0):
					c.execute("""INSERT INTO "Curso"("Asignatura", "fechaInicio", "fechaFinalizacion") values('%s','%s','%s');""" %(info[0],info[1],info[2]))
			conn.commit()
			print("Cursos ok")

		if add_alumno:
			conn.commit()
			Curs = []
			for i in range(alumnos):
				item = [random_dni(),fake.first_name(),fake.last_name(),fake.last_name(), fake.free_email(), random.choice([True, False])]
				#item = ['12345678V',fake.first_name(),fake.last_name(),fake.last_name(), fake.free_email(), False]
				r = c.execute("""SELECT count(*) from "Alumno" where "dni" =  '%s';""" %(item[0]))
				result=c.fetchone()
				if result[0] == 0:
					c.execute("""INSERT INTO "Alumno"("dni", "nombre", "apellido1", "apellido2","email","repetidor") 
		        		values('%s','%s','%s','%s','%s','%s');""" %(item[0],item[1],item[2],item[3],item[4],item[5]))
			conn.commit()
			print("Alumno ok")

		if add_Curso_alumno:
			c.execute("""SELECT "dni" from "Alumno";""")
			Alumno = c.fetchall()
			alumno_id = random.choice([i[0] for i in Alumno])
			#print(Alumno)
			c.execute("""SELECT "Asignatura" from "Curso";""")
			Curs = c.fetchall()
			curso_id = random.choice([i[0] for i in Curs])
			id = 1
			for i in Alumno:
				#alumno_id = [i[0] in Alumno]
				alumno_id = random.choice([i[0] for i in Alumno])
				curso_id = random.choice([i[0] for i in Curs])
				c.execute("""INSERT INTO "tfg_curso_alumno"("id", "Alumno_id", "Curso_id") values('%s','%s','%s');""" %(id,alumno_id,curso_id))

				id = id + 1
			conn.commit()
			print("Asociativa curso-alumno ok")

		if add_profesor:
			for i in range(Profesores):
				item = [fake.ean(length=8),fake.first_name(),fake.last_name(),fake.last_name()]
				#item = ['12345678',fake.first_name(),fake.last_name(),fake.last_name()]
				r = c.execute("""SELECT count(*) from "Profesor" where "PDI" =  '%s';""" %(item[0]))
				result=c.fetchone()
				if result[0] == 0:
					c.execute("""INSERT INTO "Profesor"("PDI", "nombre", "apellido1", "apellido2") values('%s','%s','%s','%s');""" %(item[0],item[1],item[2],item[3]))
			conn.commit()
			print("Profesor ok")

		if add_encuesta:
			c.execute("""SELECT "PDI" from "Profesor";""")
			Profesor = c.fetchall()
			c.execute("""SELECT "id" from "tfg_curso_alumno";""")
			Curs = c.fetchall()
			id = 1
			for i in Profesor:
				profesor_id = random.choice([i[0] for i in Profesor])
				curso_id = random.choice([i[0] for i in Curs])
				c.execute("""INSERT INTO "tfg_encuesta"("id", "Nota", "Curso_alumno_id","Profesor_id") values('%s','%s','%s','%s');""" %(id,randint(0,10),curso_id,profesor_id))
				id = id + 1
			conn.commit()
			print("Asociativa Encuesta ok")

		if add_practica:
			practicas_disponibles = ['practica 1', 'practica 2','practica 3','practica 4','practica 5','practica 6','practica 7','practica 8','practica 9','practica 10','practica 11','practica 12','practica 13','practica 14','practica 15','practica 16','practica 17',]
			for i in range(practicas):
				info = [(random.choice(practicas_disponibles)),fake.date_between(start_date="today", end_date="+1y")]
				if True:
					r = c.execute("""SELECT count(*) from "tfg_practica" where "Nom" =  '%s';""" %(info[0]))
					result=c.fetchone()
				if (result[0] == 0):
					c.execute("""INSERT INTO "tfg_practica"("Nom", "Fecha") values('%s','%s');""" %(info[0],info[1]))
			conn.commit()
			print("Practicas ok")

		if add_nivel:
			c.execute("""SELECT "Nom" from "tfg_practica";""")
			Practicas = c.fetchall()
			metodos_disponibles = ['SQL injection', 'XSS', 'envenenamiento de cookies','buffer overflow', 'metadatos',
			'scripting','algorithmia','fuerza bruta','NTP','Phishing','Keylogger','Malware','Ataque por Diccionario','Ingenieria social','Spidering']
			hint_disponibles = ['revisa el reloj','prueba a ejecutar html','revisa el componente JavaScript',
			'Puede que haya algo que no deba estar','prueba con la base de datos','Un error que podriar hacer cualquier humano...', 'El usuario siempre, siempre utiliza la misma contrasenya para todas sus cuentas']
			for i in range(niveles):
				practica_id = random.choice([i[0] for i in Practicas])
				info = [randint(1,niveles),(random.choice(metodos_disponibles)),(random.choice(hint_disponibles))]
				if True:
					r = c.execute("""SELECT count(*) from "Nivel" where "numero" =  '%s';""" %(info[0]))
					result=c.fetchone()
				if (result[0] == 0):
					c.execute("""INSERT INTO "Nivel"("numero", "metodo", "hint", "Practica_id") values('%s','%s','%s','%s');""" %(info[0],info[1],info[2],practica_id))
			conn.commit()
			print("Niveles ok")

		if add_completado:
			c.execute("""SELECT "dni" from "Alumno";""")
			Alumno = c.fetchall()
			c.execute("""SELECT "numero" from "Nivel";""")
			Niveles = c.fetchall()
			id = 1
			for i in Alumno:
				alumno_id = random.choice([i[0] for i in Alumno])
				niveles_id = random.choice([i[0] for i in Niveles])
				c.execute("""INSERT INTO "Completado"("id", "completado", "Alumno_id","Nivel_id") values('%s','%s','%s','%s');""" %(id,bool(random.getrandbits(1)),alumno_id,niveles_id))
				id = id + 1
			conn.commit()
			print("Asociativo Completado ok")

		if add_nota:
			c.execute("""SELECT "dni" from "Alumno";""")
			Alumno = c.fetchall()
			c.execute("""SELECT "Nom" from "tfg_practica";""")
			Practicas = c.fetchall()
			id = 1
			for i in Alumno:
				alumno_id = random.choice([i[0] for i in Alumno])
				practicas_id = random.choice([i[0] for i in Practicas])
				c.execute("""INSERT INTO "Nota"("id","Nota", "Alumno_id","Practica_id") values('%s','%s','%s','%s');""" %(id,randint(0,10),alumno_id,practicas_id))
				id = id + 1
			conn.commit()
			print("Asociativo Nota ok")

		if add_con_passwd:
			c.execute("""SELECT "numero" from "Nivel";""")
			Niveles = c.fetchall()
			for i in Niveles:
				nivel_id = random.choice([i[0] for i in Niveles])
				r = c.execute("""SELECT count(*) from "NivelConPassword" where "nivel_id" =  '%s';""" %(nivel_id))
				result=c.fetchone()
				if (result[0] == 0):
					c.execute("""INSERT INTO "NivelConPassword"("nivel_id","Usuario", "password") values('%s','%s','%s');""" %(nivel_id,fake.user_name(),fake.user_name()))
			conn.commit()
			print("Password ok")
		if add_sin_passwd:
			c.execute("""SELECT "numero" from "Nivel";""")
			elementos = ['Buscador', 'Cookie', 'Complemento Java', 'Mail', 'Reloj']
			Niveles = c.fetchall()
			for i in Niveles:
				nivel_id = random.choice([i[0] for i in Niveles])
				r = c.execute("""SELECT count(*) from "NivelSinPassword" where "nivel_id" =  '%s';""" %(nivel_id))
				result=c.fetchone()
				if (result[0] == 0):
					c.execute("""INSERT INTO "NivelSinPassword"("nivel_id","elemento") values('%s','%s');""" %(nivel_id,(random.choice(elementos))))
			conn.commit()
			print("Sin password ok")

		c.execute("""CREATE index al on "Alumno"("dni", "nombre", "apellido1", "apellido2","email","repetidor"); """)
		conn.commit()

		print("cerrando conexion")
		c.close()
		conn.close()