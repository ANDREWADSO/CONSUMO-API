from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from .models import *
from django.utils.timezone import now
from django.db.models import Q
# IMPORTACIONES PARA EL LOGIN
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .forms import LoginForm, UserRegistrationForm




# Create your views here.
TEMPLATE_DIRS=(
    
    'os.path.join(BASE_DIR, "templates")'
)
def index (request):
    return render(request,"index.html")

def listar (request):
    if request.method == "POST": 
        palabra = request.POST.get('keyword')
        lista = Usuarios.objects.all()
        
        if palabra is not None:
            resultado_busqueda = lista.filter(
                Q(id_iconstains=palabra)|
                Q(nombre_icontains =palabra)|
                Q(apellido_icontains=palabra)|
                Q(correo_icontains= palabra)|
                Q(telefono_icontains=palabra)
            )
    
            datos = {'usuarios': resultado_busqueda}
            return render(request, "crud_usuarios/listar.html", datos)
        else:
            datos = {'usuarios': lista}
            return render(request,"crud_usuarios/listar.html", datos)
            
        
    else:
        users = Usuarios.objects.order_by('-id')[:10]
        datos = {'usuarios': users}
        return render(request,"crud_usuarios/listar.html", datos)

def agregar (request):
    if request.method == "POST":
        #AGREGO LOS DATOS
        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get ('correo') and request.POST.get('telefono') and request.POST.get('fecha_nacimiento'):
            user = Usuarios()
            user.nombre= request.POST.get('nombre')
            user.apellido= request.POST.get('apellido')
            user.correo= request.POST.get('correo')
            user.telefono= request.POST.get('telefono')
            user.fecha=request.POST.get('fecha')
            user.save()
        return redirect ('listar')
    else: 
        
     return render(request,"crud_usuarios/agregar.html")

def actualizar (request, idUsuario):
    try:
        if request.method== 'POST':
            if request.POST.get('id') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get ('correo') and request.POST.get('telefono') and request.POST.get('fecha_nacimiento'):
                user_id_old= request.POST.get('id')
                user_old = Usuarios()
                user_old= Usuarios.objects.get(id= user_id_old)
            
                user = Usuarios()
                user.id= request.POST.get('id')
                user.nombre= request.POST.get('nombre')
                user.apellido= request.POST.get('apellido')
                user.correo= request.POST.get('correo')
                user.telefono= request.POST.get('telefono')
                user.fecha_nacimiento=request.POST.get('fecha')
                user.fecha_registro = user_old.fecha_registro
                user.save()
            return redirect ('listar')
        
        else:
            users = Usuarios.objects.all()
            user = Usuarios.objects.get(id= idUsuario)
            datos = {'usuarios': users, 'usuario': user}    
            return render(request,"crud_usuarios/actualizar.html", datos)
        
    except  Usuarios.DoesNotExist:
            users = Usuarios.objects.all()
            user = None
            datos = {'usuarios': users, 'usuario': user}  
            return render(request,"crud_usuarios/actualizar.html", datos)
        
def eliminar (request, idUsuario):
    try:
        if request.method=='POST':
                if request.POST.get('id'):
                    id_a_borrar= request.POST.get('id')
                    tupla = Usuarios.objects.get(id = id_a_borrar)
                    tupla.delete()
                    return redirect('listar')
        else:
            users = Usuarios.objects.all()
            user= Usuarios.objects.get(id= idUsuario)
            datos = {'usuarios': users, 'usuario': user} 
            return render(request,"crud_usuarios/eliminar.html", datos)
        
    except Usuarios.DoesNotExist:
            users = Usuarios.objects.all()
            user= None
            datos = {'usuarios': users, 'usuario': user} 
            return render(request,"crud_usuarios/eliminar.html",datos)
        
        

def preguntas (request):
    response= requests.get ('https://backend-final1.onrender.com/api-auth/api/preguntas/').json()
    print (response)
    # Aquí va la lógica para obtener y procesar las preguntas
    # por ejemplo, puedes obtener las preguntas de la base de datos o de otro lugar
    preguntas = ['¿Cuál es tu color favorito?', '¿Cuál es tu comida favorita?', '¿Cuál es tu película favorita?']
    
    # Renderiza la plantilla y pasa las preguntas como contexto
    return render(request, 'preguntas.html', {'preguntas': response})

def estilos (request):
    return render(request,"estilos.html")



#CODIGO OBTENIDO DE LOGIN DE USUARIOS:

def landing_page(request):
    return render(request, 'landing_page.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password']) # None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('El usuario no esta activo')
            else:
                return HttpResponse('La información no es correcta')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    
@login_required
def dashboard(request):
    return render(request, 
                  'account/dashboard.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 
                      'account/register.html',
                      {'user_form': user_form})
    
def profile_view(request):
    # Aquí puedes obtener los datos del usuario actualmente autenticado
    user = request.user
    context = {
        'user': user,
        # otros datos que desees pasar al template
    }
    return render(request, 'profile.html', context)