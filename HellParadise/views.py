#region imports
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
    return render(request, 'index.html')

#region usuario
def registro_usuario(request):
    if request.method=='POST':
        user=authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password'):
            usuario = User.objects.create_user(request.POST.get('username'),request.POST.get('email'),request.POST.get('password'))
            usuario.first_name = request.POST.get('nombre')
            usuario.last_name = request.POST.get('apellido')
            usuario.save()
            return redirect('login')
    else:
        return render(request, 'usuario/registro_usuario.html')

def loginusuario(request):
    if request.method == "POST":
        usuario = request.POST.get('usuario')
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
def insertar_categoria(request):
    if request.method == "POST":
        if request.POST.get('nombre'):
            categoria = Categoria()
            categoria.nombre = request.POST.get('nombre')
            categoria.save()
            return redirect('lista_categoria')
    else:
        categoria = Categoria.objects.all()
        return render(request, 'producto/insertar_categoria.html', {'categoria': categoria})

def actualizar_categoria(request, id_categoria):
        if request.method == 'POST':
                categoria = Categoria.objects.get(id=id_categoria)
                categoria.nombre = request.POST.get('nombre')
                categoria.save()
                return redirect('lista_categoria')
        else:
            un_categoria = Categoria.objects.filter(id=id_categoria)
            return render(request, 'producto/actualizar_categoria.html', {'un_categoria': un_categoria})

def listado_categoria(request):
    categorias = Categoria.objects.all
    return render(request, "producto/listado_categoria.html", {"categorias": categorias})

def eliminar_categoria(request,id_categoria):
        eliminar_categoria = Categoria.objects.get(id=id_categoria)
        eliminar_categoria.delete()
        return redirect('lista_categoria')
#endregion

#region producto
def insertar_producto(request):
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
                imagen_pillow = imagen_pillow.convert('RGB').save('new.jpeg')
            
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

            return redirect('insertar_producto')
    else:
        categorias = Categoria.objects.all()
        return render(request, 'producto/insertar_producto.html', {'categoria': categorias}) 

def listado_producto(request):
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

    return render(request, "producto/listado_producto.html", {'productos': productos})

def actualizar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    print("antes de if")

    if request.method == "POST":
        print("despues del if")
        # Recopila todos los datos del formulario
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        producto.categoria_id = request.POST.get('categoria_id')
        producto.talla = request.POST.get('talla')
        producto.color = request.POST.get('color')

        # Procesa la imagen con Pillow si es necesario
        
        if request.POST.get('imagenes') != "":
            imagen = request.FILES['imagenes']
            imagen_pillow = Image.open(imagen).convert('RGB')

            # Convertir la imagen a modo RGB si está en modo RGBA
            if imagen_pillow.mode == 'RGBA':
                imagen_pillow = imagen_pillow.convert('RGB').save('new.jpeg')

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
            
            producto.save() 
        
        # Guarda el producto actualizado en la base de datos
        producto.save()

        return redirect('/producto/listado_producto/')  # Reemplaza con tu URL de listado de productos

    categorias = Categoria.objects.all()
    return render(request, 'producto/actualizar_producto.html', {'categoria': categorias, 'producto': producto})


def eliminar_producto(request,id_producto):
    eliminar_producto = Producto.objects.get(id=id_producto)
    eliminar_producto.delete()
    return redirect('lista_producto')

#endregion