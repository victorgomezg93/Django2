# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.core.exceptions import ValidationError

from django.db import models

# Create your models here.

class Curso(models.Model):
	Asignatura = models.CharField('Asignatura y any',max_length=200,primary_key=True)
	fechaInicio = models.DateField('Inicio de curso')
	fechaFinalizacion = models.DateField('Final de curso')
	Alumno = models.ManyToManyField('Alumno',through='Curso_alumno', through_fields=('Curso','Alumno'))

	class Meta:
		db_table = "Curso"
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'

	def __str__(self):
		return self.Asignatura


class Profesor(models.Model):
	PDI = models.CharField(max_length=9,primary_key=True)
	nombre = models.CharField(max_length=100)
	apellido1 = models.CharField('Primer apellido',max_length=50)
	apellido2 = models.CharField('Segundo apellido',max_length=50)
	Curso_alumno = models.ManyToManyField('Curso_alumno', through='Encuesta', through_fields=('Profesor','Curso_alumno'))

	def __str__(self):
		return self.PDI

	class Meta:
		db_table = "Profesor"
		verbose_name = 'Profesor'
		verbose_name_plural = 'Profesores'
		unique_together = ("nombre", "apellido1", "apellido2")

class Practica(models.Model):
	Nom = models.CharField('Nom de la practica',max_length=200,primary_key=True)
	Fecha = models.DateField('echa de entrega')
	Alumno = models.ManyToManyField('Alumno', through='Nota', through_fields=('Practica','Alumno'))

	def __str__(self):
		return self.Nom

class Nivel(models.Model):
	numero = models.IntegerField(primary_key=True)
	metodo = models.CharField(max_length=100)
	hint = models.CharField(max_length=100)
	Practica = models.ForeignKey(Practica, on_delete=models.PROTECT)
	Alumno = models.ManyToManyField('Alumno',through='Completado', through_fields=('Nivel','Alumno'))

	def __str__(self):
		return str(self.numero)

	class Meta:
		db_table = "Nivel"
		verbose_name = 'Nivel'
		verbose_name_plural = 'Niveles'
		ordering = ['numero']

class NivelConPassword(models.Model):
	nivel = models.OneToOneField(Nivel, verbose_name=('Nivel'),primary_key=True,on_delete=models.CASCADE)
	Usuario = models.CharField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return str(self.nivel)

	class Meta:
		db_table = "NivelConPassword"
		verbose_name = 'NivelConPassword'
		verbose_name_plural = 'NivelesConPassword'
		unique_together = ("Usuario", "password")

class NivelSinPassword(models.Model):
	nivel = models.OneToOneField(Nivel, verbose_name=('Nivel'),primary_key=True,on_delete=models.CASCADE)
	elemento = models.CharField(max_length=100)

	def __str__(self):
		return str(self.nivel)

	class Meta:
		db_table = "NivelSinPassword"
		verbose_name = 'NivelSinPassword'
		verbose_name_plural = 'NivelesSinPassword'


class Alumno(models.Model):
	dni = models.CharField(max_length=9,primary_key=True)
	nombre = models.CharField(max_length=100)
	apellido1 = models.CharField('Primer apellido',max_length=50)
	apellido2 = models.CharField('Segundo apellido',max_length=50)
	email = models.EmailField("Correo electronico",null=True)
	repetidor = models.BooleanField()
	curs = models.ManyToManyField(Curso, blank=True, related_name="Historico_de_cursos")
	Nivel = models.ManyToManyField('Nivel', through = 'Completado',through_fields=('Alumno','Nivel'))
	Practica = models.ManyToManyField('Practica', through = 'Nota',through_fields=('Alumno','Practica'))
	Curso = models.ManyToManyField('Curso',through = 'Curso_alumno',through_fields=('Alumno','Curso'))


	def __str__(self):
		return self.dni

	class Meta:
		db_table = "Alumno"
		verbose_name = 'Alumno'
		verbose_name_plural = 'Alumnos'
		unique_together = ("nombre", "apellido1", "apellido2")

#taula intermitja per crear l'associació ternaria, guardarem el curs del alumne
class Curso_alumno(models.Model):
	id= models.AutoField(primary_key=True)
	Alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
	Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	Profesor = models.ManyToManyField('Profesor', through = 'Encuesta',through_fields=('Curso_alumno','Profesor'))

	def __str__(self):
		return str(self.Alumno.dni) + " Curso:" + str(self.Curso.Asignatura)

	def clean(self):
		Direct = Curso_alumno.objects.filter(Curso = self.Curso, Alumno = self.Alumno)
		if Direct.exists():
			raise ValidationError('Esta asociacion ya existe, eliminala para volverla a introducir')

class Encuesta(models.Model):
	id = models.AutoField(primary_key=True)
	Nota = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
	Profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
	Curso_alumno = models.ForeignKey(Curso_alumno, on_delete=models.CASCADE)
	
	def __str__(self):
		return "Profesor: " + str(self.Profesor.PDI) + " Alumno: " + str(self.Curso_alumno.Alumno) + " Curso: " + str(self.Curso_alumno.Curso)
		return str(self.id)

	def clean(self):
		Direct = Encuesta.objects.filter(Profesor = self.Profesor, Curso_alumno = self.Curso_alumno)
		if Direct.exists():
			raise ValidationError('Esta encuesta ya existe, eliminala para volverla a introducir')

class Completado(models.Model):
	id= models.AutoField(primary_key=True)
	completado = models.BooleanField()
	Alumno = models.ForeignKey(Alumno, to_field ='dni', on_delete=models.CASCADE)
	Nivel = models.ForeignKey(Nivel, to_field ='numero', on_delete=models.CASCADE)

	def clean(self):
		Direct = Completado.objects.filter(Alumno = self.Alumno, Nivel = self.Nivel)
		if Direct.exists():
			raise ValidationError('Esta asociacion ya existe, eliminala para volverla a introducir')

	def __str__(self):
		return str(self.Alumno.dni) + " Nivel:" + str(self.Nivel.numero)

	class Meta:
		db_table = "Completado"
		verbose_name = 'Completado'
		verbose_name_plural = 'Completados'
		unique_together = ("Alumno", "Nivel")

class Nota(models.Model):
	id= models.AutoField(primary_key=True)
	Nota = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
	Alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
	Practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
	completado = models.ManyToManyField(Completado, blank=True)

	def __str__(self):
		return str(self.Alumno.dni) + " Practica:" + str(self.Practica.Nom)

	def clean(self):
		Direct = Nota.objects.filter(Alumno = self.Alumno, Practica = self.Practica)
		if Direct.exists():
			raise ValidationError('Esta nota ya existe, eliminala para volverla a introducir')

	class Meta:
		db_table = "Nota"
		verbose_name = 'Nota'
		verbose_name_plural = 'Notas'
		unique_together = ("alumno", "practica")

#
