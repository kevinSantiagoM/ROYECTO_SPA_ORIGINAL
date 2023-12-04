from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import login_view, register_view,user_list_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('',views.inicio, name='inicio'),
    path('logout/', views.signout, name='Salir'),
    path('register/', register_view, name='register'),
    path('userregistrados/', user_list_view, name='user_list'),
    path('Menu', views.Menu, name='Menu'),

    path('citas_agendadas', views.lista_citas, name='lista_citas'),
    path('servicio_cliente/', views.servicio_cliente, name='servicio_cliente'),
    path('promociones/', views.promociones, name='promociones'),

    path('galeria/', views.galeria, name='galeria'), 
    path('contacto/', views.contacto, name='contacto'),


    #----------------Administrador-------------------
    path('Servicios_agendados/', views.Servicios, name='Servicios_agendados'),
    path('Promociones_agendadas/', views.Promociones_agendadas, name='Promociones_agendadas'),
    path('Historial_admin/', views.Historial_admin, name='Historial_admin'),
    path('Agregar_servicio/', views.añadir_Servicios, name='Agregar_Servicio'),
    path('Agendar_Promociones/', views.Agendar_Promociones, name='Agendar_Promociones' ),
    path('Agregar_galeria/', views.Agregar_galeria, name='Agregar_galeria'),
    

    path('crear/', views.crear_cita, name='crear_cita'),
    path('editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('eliminar_cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('eliminar_cita_promo/<int:cita_id>/', views.eliminar_cita_promo, name='eliminar_cita_promo'),
    path('editar_servicio/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar_servicio/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('editar_promocion/<int:promocion_id>/', views.editar_promocion, name='editar_promocion'),

    path('eliminar_imagenes/', views.eliminar_imagenes, name='eliminar_imagenes'),
        #-------------------Eliminar Promocion-------------------------------------------------
    path('eliminar_promocion/<int:promocion_id>/', views.eliminar_promocion, name='eliminar_promocion'),


    path('base_admin/', views.base_admin, name='base_admin'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)