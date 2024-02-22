from django.db import models

# Modelo para Usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    class Meta:
        db_table = 'usuarios'

# Modelo para Categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'categorias'

# Modelo para Productos
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagenes = models.ImageField(upload_to='', blank=True, null=True)
    talla = models.CharField(max_length=10)
    color = models.CharField(max_length=50)

    class Meta:
        db_table = 'productos'

# Modelo para Pedidos
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)

    class Meta:
        db_table = 'pedidos'

# Modelo para Detalles de Pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detallespedido'

# Modelo para Comentarios y Calificaciones
class ComentarioCalificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField()

    class Meta:
        db_table = 'comentarioscalificaciones'

# Modelo para Métodos de Pago
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'metodospago'

# Modelo para Métodos de Envío
class MetodoEnvio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'metodosenvio'
