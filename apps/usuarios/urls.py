from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('Registro/', views.Registro.as_view(), name = 'registro'),

    path('Perfil/<int:pk>/', views.Perfil, name = 'perfil'),

]