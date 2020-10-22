# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import Alumno, Profesor, Curso
from django.template import loader

from .models import *
from .forms import *
from tfg.models import Alumno as Alumno
import django_tables2 as tables

# Create your views here.

def alumno_view(request):
    if request.method == 'POST':
        form = AlumnoForm2(request.POST)
        if form.is_valid():
            form.save()
        return redirect("alumno.html")
    else:
        form = AlumnoForm2()

    return render(request,"alumno.html")

def add_alumno_form_submision(request):
	if request.method == 'POST':
		form = AlumnoForm2(request.POST)
		if form.is_valid():
			form.save()
		return redirect("/alumno")
	else:
		form = AlumnoForm2()
	return render(request,"alumno.html")

class crea_alumno(CreateView):
	model = Alumno
	form_class = AlumnoForm2
	template_name = 'alumno3.html'
	success_url = reverse_lazy('mostrar_alumnos')

class crea_profe(CreateView):
	model = Profesor
	form_class = ProfesorForm
	template_name = 'profesor3.html'
	success_url = reverse_lazy('mostrar_profesores')

class crea_curso(CreateView):
	model = Curso
	form_class = CursoForm
	template_name = 'curso3.html'
	success_url = reverse_lazy('mostrar_cursos')

def index(request):
	return render(request,'index.html')

def add_profesor_form_submision(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/profesor")
    else:
        form = ProfesorForm()

    return render(request,"profesor.html")

def add_curso_form_submision(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/cursos")	
    else:
        form = CursoForm()

    return render(request,"cursos.html")


def mostrar_alumnos2(request):
	alumnos = Alumno.objects.all()
	return render(request, 'mostrar_alumnos.html', {'alumnos': alumnos})

def mostrar_alumnos(request):
	alumnos = Alumno.objects.all()
	return render(request, 'mostrar_alumnos.html', {'alumnos': alumnos})

def mostrar_profesores2(request):
	profesores = Profesor.objects.all()
	return render(request, 'mostrar_profesores.html', {'profesores': profesores})

def mostrar_cursos2(request):
	cursos = Curso.objects.all()
	return render(request, 'mostrar_cursos.html', {'cursos': cursos})

def alumno_delete(request):
	username = request.POST['dni']
	user = Alumno.objects.get(dni=username)
	if request.method == 'POST':
		user.delete()
		return redirect('delete')
	return render(request, 'delete')

def profesor_delete(request):
	username = request.POST['PDI']
	user = Profesor.objects.get(PDI=username)
	if request.method == 'POST':
		user.delete()
		return redirect('delete')
	return render(request, 'delete')

def curso_delete(request):
	username = request.POST['Asignatura']
	user = Curso.objects.get(Asignatura=username)
	if request.method == 'POST':
		user.delete()
		return redirect('delete')
	return render(request, 'delete')

def alumno_update(request):
	username = request.POST['dni']
	user = Alumno.objects.get(dni=username)
	form = AlumnoForm2(instance = user)
	if form.is_valid():
		user = form.save(comit = False)
		user.save()
	return redirect(request, 'edit_alumno',{'user' : user})

def alumno_update2(request):
	username = request.POST['dni']
	user = Alumno.objects.get(dni=username)
	if request.method == 'POST':
		return redirect(request, 'edit_alumno',{'user' : user})
	return render(request, 'actualizar')

def edit_alumno2(request):
	username = request.POST['dni']
	user = Alumno.objects.get(dni=username)
	return render(request, '/edit.html', {'user': user})

def edit_alumno3(request, pk):
	user = Alumno.objects.get(dni=pk)
	if request.method == 'GET':
		form = AlumnoForm2(instance=user)
	else:
		form = AlumnoForm2(request.POST, instance=user)
		if form.is_valid():
			form.save()
		return redirect('edit.html', {'form': form})
	return render(request, '/edit.html', {'form': form})

def control_alumno_edit(request, pk):
	user = get_object_or_404(Alumno, dni=pk)
	if request.method == 'POST':
		form = AlumnoForm2(request.POST, instance=user)
		if form.is_valid():
			form.save()
			dni = user.dni
			nombre = user.nombre
			apellido1 = user.apellido1
			apellido2 = user.apellido2
			email = user.email
			repetidor = user.repetidor
		return redirect('edit2.html', pk=user.dni)
	else:
		form = AlumnoForm2(instance =user)

	context = {
		"form":form,
	}
	template = 'edit2.html'
	return render(request,template,context)

def edit_post(request,slug):
	usern = get_object_or_404(Alumno, dni=slug)
	form = AlumnoForm2(request.POST, instance=usern)
	if form.is_valid():
		usern.save()
		return redirect('mostrar_alumnos')
	else:
		form = AlumnoForm2(instance=usern)
		template = 'edit2.html'
		context = {'form': form}
	return render(request,template,context)

def edit_profe(request,slug):
	usern = get_object_or_404(Profesor, PDI=slug)
	form = ProfesorForm(request.POST, instance=usern)
	if form.is_valid():
		usern.save()
		return redirect('mostrar_profesores')
	else:
		form = ProfesorForm(instance=usern)
		template = 'edit3.html'
		context = {'form': form}
	return render(request,template,context)

def edit_curso(request,slug):
	usern = get_object_or_404(Curso, Asignatura=slug)
	form = CursoForm(request.POST, instance=usern)
	if form.is_valid():
		usern.save()
		return redirect('mostrar_cursos')
	else:
		form = CursoForm(instance=usern)
		template = 'edit5.html'
		context = {'form': form}
	return render(request,template,context)

class crea_curso_alumno(CreateView):
	model = Curso_alumno
	form_class = tfg_curso_alumnoForm
	template_name = 'tfg_curso_alumno.html'
	success_url = reverse_lazy('mostrar_curso_alumno')

def m_curso_alumno(request):
	cursos = Curso_alumno.objects.all()
	return render(request, 'mostrar_curso_alumno.html', {'cursos': cursos})

class curso_alumno_delete(DeleteView):
	model = Curso_alumno
	template_name = 'd_curso_alumno.html'
	success_url = reverse_lazy('mostrar_curso_alumno')

class curso_alumno_update(UpdateView):
    model = Curso_alumno
    form_class = tfg_curso_alumnoForm
    template_name = 'tfg_curso_alumno.html'
    success_url = reverse_lazy('mostrar_curso_alumno')

class alumno_delete2(DeleteView):
	model = Alumno
	template_name = 'd_alumno.html'
	success_url = reverse_lazy('mostrar_alumnos')

class profesor_delete2(DeleteView):
	model = Profesor
	template_name = 'd_profesor.html'
	success_url = reverse_lazy('mostrar_profesores')

class curso_delete2(DeleteView):
	model = Curso
	template_name = 'd_curso.html'
	success_url = reverse_lazy('mostrar_cursos')

class alumno_edit3(UpdateView):
    model = Alumno
    form_class = AlumnoForm2
    template_name = 'alumno3.html'
    success_url = reverse_lazy('mostrar_alumnos')

class profe_edit3(UpdateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'profesor3.html'
    success_url = reverse_lazy('mostrar_profesores')

class curs_edit3(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso3.html'
    success_url = reverse_lazy('mostrar_cursos')

class crea_encuesta(CreateView):
	model = Encuesta
	form_class = tfg_EncuestaForm
	template_name = 'encuesta.html'
	success_url = reverse_lazy('mostrar_encuestas')

def m_encuestas(request):
	encuestas = Encuesta.objects.all()
	return render(request, 'mostrar_encuestas.html', {'encuestas': encuestas})

class encuesta_edit(UpdateView):
    model = Encuesta
    form_class = tfg_EncuestaForm
    template_name = 'encuesta.html'
    success_url = reverse_lazy('mostrar_encuestas')

class encuesta_delete(DeleteView):
	model = Encuesta
	template_name = 'encuesta_delete.html'
	success_url = reverse_lazy('mostrar_encuestas')
