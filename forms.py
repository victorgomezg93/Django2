from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.forms import ModelForm
from tfg.models import Alumno, Profesor, Curso
from tfg.models import *
    

class AlumnoForm(ModelForm):
    dni = forms.TextInput()
    nombre = forms.TextInput()
    apellido1 = forms.TextInput()
    apellido2 = forms.TextInput()
    email = forms.EmailField()
    repetidor = forms.BooleanField(label='myLabel', required=False,initial=False)

    class Meta:
        model = Alumno
        fields = ['dni', 'nombre', 'apellido1', 'apellido2','email','repetidor']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
)
class AlumnoForm2(forms.ModelForm):
    class Meta:
        model = Alumno
        #fields = ['dni', 'nombre', 'apellido1', 'apellido2','email','repetidor']
        fields = ['dni', 'nombre', 'apellido1', 'apellido2','email','repetidor','curs']

        labels = {
            'dni': 'dni',
            'nombre': 'nombre',
            'apellido1': 'Primer Apellido',
            'apellido2': 'Segundo Apellido',
            'email': 'Email',
            'repetidor': 'repetidor',
            'curs': 'curs'
        }

        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'repetidor': forms.CheckboxInput(attrs={'class':'form-control-checkbox','id': 'repetidor'}),
            'curs':forms.CheckboxSelectMultiple(),
        }

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['PDI', 'nombre', 'apellido1', 'apellido2']

        labels = {
            'PDI': 'PDI',
            'nombre': 'nombre',
            'apellido1': 'Primer Apellido',
            'apellido2': 'Segundo Apellido',
        }

        widgets = {
            'PDI': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['Asignatura', 'fechaInicio', 'fechaFinalizacion']

        labels = {
            'Asignatura': 'Asignatura',
            'fechaInicio': 'fecha de Inicio',
            'fechaFinalizacion': 'fecha de Finalizacion',
        }

        widgets = {
            'Asignatura': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaInicio': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaFinalizacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class tfg_curso_alumnoForm(forms.ModelForm):
    class Meta:
        model = Curso_alumno
        fields = ['id', 'Alumno', 'Curso']

        labels = {
            'id': 'id',
            'Alumno': 'Alumno',
            'Curso': 'Curso',
        }

        widgets = {
            'id': forms.NumberInput(attrs={'class': 'form-control'}),
            'Alumno': forms.Select(attrs={'class': 'form-control'}),
            'Curso': forms.Select(attrs={'class': 'form-control'}),
        }

class tfg_EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['id', 'Nota', 'Profesor', 'Curso_alumno']

        labels = {
            'id': 'id',
            'Nota': 'Nota',
            'Profesor': 'Profesor',
            'Curso_alumno': 'Curso_alumno',
        }

        widgets = {
            'id': forms.NumberInput(attrs={'class': 'form-control'}),
            'Nota': forms.NumberInput(attrs={'class': 'form-control'}),
            'Profesor': forms.Select(attrs={'class': 'form-control'}),
            'Curso_alumno': forms.Select(attrs={'class': 'form-control'}),
        }
