from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('registro_usuario/', views.registro_usuario, name="registro_usuario" ),
    path('logout/', views.logoutusuario, name="logout" ),
    path('login/', views.loginusuario, name="login"),
    path('insertar_categoria/', views.insertar_categoria, name="insertar_categoria" ),
    path('insertar_producto/', views.insertar_producto, name="insertar_producto" ),
    path('producto/listado_categoria/', views.listado_categoria, name="lista_categoria"),
    path('producto/actualizar_categoria/<int:id_categoria>',views.actualizar_categoria, name="actualizar_categoria"),
    path('producto/actualizar_producto/<int:id_producto>',views.actualizar_producto, name="actualizar_producto"),
    path('producto/eliminar_producto/<int:id_producto>',views.eliminar_producto, name="eliminar_producto"),
    path('producto/borrar/<int:id_categoria>/<str:nombre>',views.eliminar_categoria, name="eliminar_categoria"),
    path('producto/listado_producto/', views.listado_producto, name="lista_producto"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

