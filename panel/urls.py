from django.contrib import admin    
from django.urls import path, include
from . import views

urlpatterns = [
        
       
        
         
        
        
        
        path('', views.index, name="index.html"),    
        path('listar', views.listar, name="listar"),
        path('agregar', views.agregar, name="agregar"),
        path('actualizar/<int:idUsuario>', views.actualizar, name="actualizar"),
        path('eliminar/<int:idUsuario>', views.eliminar, name="eliminar"),
        path('preguntas/', views.preguntas, name='preguntas'),
        path('estilos/', views.estilos, name="estilos"),
        
        # PATHS OBTENIDOS DEL LOGIN DE USUARIO
        
        path('', include('django.contrib.auth.urls')),
        path('', views.landing_page, name='landing_page'),
        path('/', views.dashboard, name='dashboard'),
        path('', views.user_login, name='login'),
        path('register/', views.register, name='register'),
        path('profile/', views.profile_view, name='profile'),  
        
        
        
]
