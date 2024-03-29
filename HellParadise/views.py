#region imports
from tabulate import tabulate
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from HellParadise.models import Categoria, Producto

#endregion
def index(request):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        return render(request, 'index.html', context)
    else:
        mensaje_error = "No tienes permisos de operador para acceder a esta función."
        context['mensaje_error'] = mensaje_error
        return render(request, 'index.html', context)

#region usuario
def registro_usuario(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password'):
            usuario = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            usuario.first_name = request.POST.get('nombre')
            usuario.last_name = request.POST.get('apellido')
            usuario.save()
            return redirect('/login')
    else:
        return render(request, 'usuario/registro_usuario.html')

def loginusuario(request):
    if request.method == "POST":
        usuario = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect("/producto/listado_producto")
        else:
            mensaje = "¡Usuario o contraseña incorrectas!"
            return render(request, 'usuario/login.html', {'mensaje': mensaje})
    else:
        mensaje = ""
        return render(request, 'usuario/login.html', {'mensaje': mensaje})

def logoutusuario(request):
    logout(request)
    return redirect('/login')

#endregion

#region categoria
@login_required
def insertar_categoria(request):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        if request.method == "POST":
            if request.POST.get('nombre'):
                categoria = Categoria()
                categoria.nombre = request.POST.get('nombre')
                categoria.save()
                return redirect('/insertar_categoria/')
        else:
            categoria = Categoria.objects.all()
            context['categoria'] = categoria
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, 'producto/insertar_categoria.html', context)

@login_required
def actualizar_categoria(request, id_categoria):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        if request.method == 'POST':
            categoria = Categoria.objects.get(id=id_categoria)
            categoria.nombre = request.POST.get('nombre')
            categoria.save()
            return redirect('/producto/listado_categorias')
        else:
            un_categoria = Categoria.objects.filter(id=id_categoria)
            context['un_categoria'] = un_categoria
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, 'producto/actualizar_categoria.html', context)

@login_required
def listado_categoria(request):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        categorias = Categoria.objects.all()
        context['categorias'] = categorias
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, "producto/listado_categoria.html", context)

@login_required
def eliminar_categoria(request, id_categoria):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        eliminar_categoria = Categoria.objects.get(id=id_categoria)
        eliminar_categoria.delete()
        return redirect('/producto/listado_categorias')
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, 'index.html', context)

#endregion

#region producto
@login_required
def insertar_producto(request):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        if request.method == "POST" and request.FILES:
            if (
                request.POST.get('nombre') and
                request.POST.get('descripcion') and
                request.POST.get('precio') and
                request.POST.get('stock') and
                request.POST.get('categoria_id') and
                request.POST.get('talla') and
                request.POST.get('color')
            ):
                # Recopila todos los datos del formulario
                nombre = request.POST.get('nombre')
                descripcion = request.POST.get('descripcion')
                precio = request.POST.get('precio')
                stock = request.POST.get('stock')
                categoria_id = request.POST.get('categoria_id')
                talla = request.POST.get('talla')
                color = request.POST.get('color')

                # Crea una instancia de Producto
                producto = Producto(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    stock=stock,
                    categoria_id=categoria_id,
                    talla=talla,
                    color=color
                )

                # Procesa la imagen con Pillow si es necesario
                imagen = request.FILES['imagenes']
                imagen_pillow = Image.open(imagen)
                
                # Convertir la imagen a modo RGB si está en modo RGBA
                if imagen_pillow.mode == 'RGBA':
                    imagen_pillow = imagen_pillow.convert('RGB')
                
                imagen_pillow = imagen_pillow.resize((1200, 1200))

                # Crea un objeto BytesIO y guarda la imagen en él
                imagen_temp_io = BytesIO()
                imagen_pillow.save(imagen_temp_io, format='JPEG')

                # Crea un objeto File a partir del BytesIO
                imagen_temp = File(imagen_temp_io, name=imagen.name)

                # Asigna la imagen al campo 'imagenes' del producto
                producto.imagenes.save(imagen.name, imagen_temp, save=True)

                # Guarda el producto en la base de datos
                producto.save()

                return redirect('/insertar_producto/')
        else:
            categorias = Categoria.objects.all()
            context['categoria'] = categorias
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, 'producto/insertar_producto.html', context)

@login_required
def listado_producto(request):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        productos = Producto.objects.all()

        # Formatear el precio para tener separadores de miles con puntos
        for producto in productos:
            try:
                # Intentar convertir el precio a float
                precio_float = float(producto.precio)
                # Formatear el precio como entero
                producto.precio = '{:,.0f}'.format(precio_float)
            except (ValueError, TypeError):
                # Manejar casos en los que el precio no es un número válido
                producto.precio = 'N/A'

        context['productos'] = productos
        return render(request, "producto/listado_producto.html", context)
    else:
        mensaje_error = "No tienes permisos de operador para acceder a esta función."
        context['mensaje_error'] = mensaje_error
        return render(request, 'index.html', context)


@login_required
def actualizar_producto(request, id_producto):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        producto = Producto.objects.get(id=id_producto)

        if request.method == "POST" and request.FILES:
            # Recopila todos los datos del formulario
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion')
            producto.precio = request.POST.get('precio')
            producto.stock = request.POST.get('stock')
            producto.categoria_id = request.POST.get('categoria_id')
            producto.talla = request.POST.get('talla')
            producto.color = request.POST.get('color')

            # Procesa la imagen con Pillow si es necesario
            imagen = request.FILES['imagenes']
            imagen_pillow = Image.open(imagen)

            # Convertir la imagen a modo RGB si está en modo RGBA
            if imagen_pillow.mode == 'RGBA':
                imagen_pillow = imagen_pillow.convert('RGB')

            imagen_pillow = imagen_pillow.resize((1200, 1200))

            # Crea un objeto BytesIO y guarda la imagen en él
            imagen_temp_io = BytesIO()
            imagen_pillow.save(imagen_temp_io, format='JPEG')

            # Crea un objeto InMemoryUploadedFile a partir del BytesIO
            imagen_temp = InMemoryUploadedFile(
                imagen_temp_io, None, imagen.name, 'image/jpeg', imagen_temp_io.tell(), None
            )

            # Asigna la imagen al campo 'imagenes' del producto
            producto.imagenes = imagen_temp

            # Guarda el producto actualizado en la base de datos
            producto.save()

            return redirect('/producto/listado_producto/')  # Reemplaza con tu URL de listado de productos

        categorias = Categoria.objects.all()
        context['categoria'] = categorias
        context['producto'] = producto
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, 'producto/actualizar_producto.html', context)


@login_required
def eliminar_producto(request, id_producto):
    pertenece_al_grupo = request.user.groups.filter(name='usuario_operador').exists()
    context = {'pertenece_al_grupo': pertenece_al_grupo}

    if pertenece_al_grupo:
        eliminar_producto = Producto.objects.get(id=id_producto)
        eliminar_producto.delete()
        return redirect('/producto/listado_producto')
    else:
        context['mensaje_error'] = "No tienes permisos de operador para acceder a esta función."

    return render(request, 'index.html', context)

#endregion