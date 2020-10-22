# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alumno,Curso,Profesor,Encuesta,Practica,Nivel,NivelConPassword,NivelSinPassword,Completado,Nota,Curso_alumno

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Curso)
admin.site.register(Profesor)
admin.site.register(Encuesta)
admin.site.register(Practica)

admin.site.register(Nivel)
admin.site.register(NivelConPassword)
admin.site.register(NivelSinPassword)
admin.site.register(Completado)
admin.site.register(Nota)
admin.site.register(Curso_alumno)