"""
URL configuration for arrienda_rural project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from web import views as web_views

urlpatterns = [
    path("admin/", admin.site.urls ),
    path("", web_views.index, name="index"),
    path("contacto", web_views.contacto, name="contacto"),
    path("exito", web_views.exito, name="exito"),
    path("registro", web_views.registro, name="registro"),
    path("loggedout", web_views.logout, name="loggedout"),
    path("index", web_views.exit, name="exit"),
    path('arrendar_list/', web_views.ArrendarListView.as_view(), name='arrendar_list'),
    path('arrendar_list/arrendar/', web_views.arrendar, name='arrendar'),
    path('publicar_inmueble/', web_views.crear_inmueble, name='publicar_inmueble'),
    path('account/', web_views.user_redirect_view, name='user_redirect'),
    path('account/arrendatario/',  web_views.ArrendatarioAccountView.as_view(), name='arrendatario_account'),
    path('account/arrendador/', web_views.ArrendadorAccountView.as_view(), name='arrendador_account'),
    path('account/arrendatario/editar/<str:pk>/', web_views.ArrendatarioUpdateView.as_view(), name='arrendatario_update'),
    path('account/arrendador/editar/<str:pk>/', web_views.ArrendadorUpdateView.as_view(), name='arrendador_update'),
    path('vista_inmueble/<str:pk>/', web_views.inmueble_view, name='vista_inmueble'),
    path('inmueble/<int:inmueble_id>/confirmar_arriendo/', web_views.confirmar_arriendo, name='confirmar_arriendo'),
    path('ajax/cargar-comunas/', web_views.cargar_comunas, name='cargar_comunas'),
    path('inmueble/<int:pk>/editar/', web_views.InmuebleUpdateView.as_view(), name='editar_inmueble'),
    path('inmueble/<int:pk>/eliminar/', web_views.eliminar_inmueble, name='eliminar_inmueble'),
    path('inmueble/<int:inmueble_id>/liberar/', web_views.liberar_inmueble, name='liberar_inmueble'),
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)