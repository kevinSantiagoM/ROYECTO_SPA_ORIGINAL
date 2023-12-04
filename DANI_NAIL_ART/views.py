from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import CitaForm, Agendar_Servicio, Agendar_Galeria, Agendar_PromocionesForm
from .models import Cita, Servicio, Galeria,Promociones,CustomUser
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse,HttpResponseNotAllowed
import json
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import uuid 


def base_admin(request):
    return render(request, 'layouts/base_admin.html')

def inicio(request):
    return render(request, 'layouts/base_inicio.html')

def login_view(request):
    return render(request, 'login/inicio.html')

def signout(request):
    logout(request)
    return redirect('login')

# ... (importaciones y otras vistas)

from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # Verificar si el usuario es administrador
                if user.es_administrador:
                    return redirect('Servicios_agendados')
                else:
                    return redirect('Menu')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'Login/inicio.html', {'form': form})





def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_id = str(uuid.uuid4())

            # Establecer el campo es_administrador
            user.es_administrador = form.cleaned_data['es_administrador']

            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'Register/registrar.html', {'form': form})


def user_list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'Register/userregistrados.html', {'users': users})



def Menu(request):
    return render(request, 'Menu.html')

from django.contrib.auth.decorators import login_required

def lista_citas(request):
    citas = Cita.objects.filter(usuario=request.user)
    return render(request, 'Citas/lista_citas.html', {'citas': citas})

def servicio_cliente(request):
    servicio = Servicio.objects.all()
    return render(request, 'Servicios/Servicios_cliente.html', {
        'servicio':servicio,
    })
def promociones(request):
    promociones = Promociones.objects.all()
    return render(request, 'Promociones/Promociones.html', {'promociones': promociones})


def galeria(request):
    imagenes_galeria = Galeria.objects.all().order_by('-created_at')
    return render(request, 'Galeria/Galeria.html', {'imagenes_galeria': imagenes_galeria})

def contacto(request):
    return render(request, 'Contacto/Contacto.html')






#----------------administrador--------------------
def Servicios(request):
    servicio = Servicio.objects.all()
    return render(request, 'Servicios/Servicios_agendados.html', {
        'servicio':servicio,
    })

def Promociones_agendadas(request):
    promociones = Promociones.objects.all()
    return render(request, 'Promociones/Promociones_admin.html', {'promociones': promociones})

from datetime import date
from .models import Cita
from django.shortcuts import render

@login_required
def Historial_admin(request):
    citas = Cita.objects.all()
    today = date.today()
    return render(request, 'Citas/Historia_admin.html', {'citas': citas, 'today': today})


def añadir_Servicios( request ):
    if request.method == 'POST':
        form = Agendar_Servicio(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Servicios_agendados')
    else:
        form = Agendar_Servicio()

    return render(request, 'Servicios/Agregar_Servcios.html', {
        'form': form, 
    })

def Agendar_Promociones(request):
    if request.method == 'POST':
        form = Agendar_PromocionesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Promociones_agendadas')
    else:
        form = Agendar_PromocionesForm()

    return render(request, 'Promociones/Agregar_promo.html', {'form': form})


#------------------------CREAR CITA-------------------------------

from django.contrib.auth.decorators import login_required

@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.usuario = request.user  # Asigna el usuario actual
            cita.save()
            return redirect('lista_citas')
    else:

        nombre_servicio = request.GET.get('nombre_servicio', '')
        descripcion_servicio = request.GET.get('descripcion_servicio', '')
        precio_servicio = request.GET.get('precio_servicio', '')
        
        
        form = CitaForm(initial={
            'nombre_servicio' : nombre_servicio,
            'nombre' :nombre_servicio,
            'descripcion': descripcion_servicio,
            'precio' : precio_servicio,
            
        })

    return render(request, 'Citas/crear_cita.html', {'form': form})


#---------------------------EDITAR CITA-------------------------------------
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('lista_citas')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'Citas/editar_cita.html', {'form': form, 'cita': cita})

def editar_promocion(request, promocion_id):
    promocion = get_object_or_404(Promociones, pk=promocion_id)

    if request.method == 'POST':
        form = Agendar_PromocionesForm(request.POST, request.FILES, instance=promocion)
        if form.is_valid():
            form.save()
            return redirect('Promociones_agendadas')
    else:
        form = Agendar_PromocionesForm(instance=promocion)

    return render(request, 'Promociones/Editar_promocion.html', {'form': form, 'promocion': promocion})


def eliminar_promocion(request, promocion_id):
    try:
        prmocion = Promociones.objects.get(id=promocion_id)
        prmocion.delete()
        messages.success(request, 'La cita ha sido eliminada exitosamente.')
    except Promociones.DoesNotExist:
        messages.error(request, 'La cita no se encontró o no pudo ser eliminada.')

    return redirect(reverse('Promociones_agendadas'))




#----------------------ELIMINAR CITA----------------------------------
def eliminar_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        cita.delete()
        messages.success(request, 'La cita ha sido eliminada exitosamente.')
    except Cita.DoesNotExist:
        messages.error(request, 'La cita no se encontró o no pudo ser eliminada.')

    return redirect(reverse('lista_citas')) 

def eliminar_cita_promo(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        cita.delete()
        messages.success(request, 'La cita ha sido eliminada exitosamente.')
    except Cita.DoesNotExist:
        messages.error(request, 'La cita no se encontró o no pudo ser eliminada.')

    return redirect(reverse('Historial_admin'))



#---------------EDITAR SERVICIOS--------------------
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    
    if request.method == 'POST':
        form = Agendar_Servicio(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('Servicios_agendados')
    else:
        form = Agendar_Servicio(instance=servicio)
    return render(request, 'Servicios/editar_servicio.html', {'form': form, 'servicio': servicio})

#---------------ELIMINAR SERVICIOS---------------------
def eliminar_servicio(request, servicio_id):
    try:
        servicio = Servicio.objects.get(id=servicio_id)
        servicio.delete()
        messages.success(request, 'La cita ha sido eliminada exitosamente.')
    except Servicio.DoesNotExist:
        messages.error(request, 'La cita no se encontró o no pudo ser eliminada.')

    return redirect(reverse('Servicios_agendados'))

def eliminar_imagenes(request):
    if request.method == 'POST':
        try:
            # Obtén la lista de IDs de las imágenes a eliminar desde el cuerpo de la solicitud
            data = json.loads(request.body)
            imagenes_seleccionadas = data.get('imagenes_seleccionadas', [])

            # Elimina las imágenes seleccionadas
            Galeria.objects.filter(id__in=imagenes_seleccionadas).delete()

            # Puedes devolver una respuesta JSON indicando éxito
            return JsonResponse({'success': True})
        except Exception as e:
            # Maneja cualquier error y devuelve una respuesta JSON indicando el error
            return JsonResponse({'success': False, 'error': str(e)})

    # Maneja otras solicitudes HTTP
    return HttpResponseNotAllowed(['POST'])

def Agregar_galeria(request):
    imagenes_galeria = Galeria.objects.all()

    if request.method == 'POST':
        form = Agendar_Galeria(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Redirigir a la misma página después de guardar la nueva imagen
            return redirect('Agregar_galeria')

    else:
        # Si es una solicitud GET, simplemente renderiza el formulario y las imágenes
        form = Agendar_Galeria()

    return render(request, 'Galeria/Agregar_galeria.html', {'form': form, 'imagenes_galeria': imagenes_galeria})
