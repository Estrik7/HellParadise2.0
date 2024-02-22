"""
URL configuration for HellParadise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import actualizar_categoria, actualizar_producto, eliminar_categoria, eliminar_producto, insertar_categoria, insertar_producto, listado_categoria, listado_producto, loginusuario, logoutusuario, registro_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro_usuario/', registro_usuario ),
    path('logout/', logoutusuario ),
    path('login/', loginusuario ),
    path('insertar_categoria/', insertar_categoria ),
    path('insertar_producto/', insertar_producto ),
    path('producto/listado_categoria/', listado_categoria),
    path('producto/actualizar_categoria/<int:id_categoria>',actualizar_categoria),
    path('producto/actualizar_producto/<int:id_producto>',actualizar_producto),
    path('producto/eliminar_producto/<int:id_producto>',eliminar_producto),
    path('producto/listado_producto/', listado_producto),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

