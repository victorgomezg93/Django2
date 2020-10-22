from django.urls import path
from tfg.views import *

app_name = 'tfg'
urlpatterns = [
	path('', index, name='index'),
]