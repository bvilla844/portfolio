from django.db import models
import django
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = [
    ('electronica', 'Electrónica'),
    ('celulares', 'Celulares y Accesorios'),
    ('computacion', 'Computación'),
    ('consolas_videojuegos', 'Consolas y Videojuegos'),
    ('televisores', 'Televisores y Audio'),
    ('electrodomesticos', 'Electrodomésticos'),
    ('hogar_muebles', 'Hogar y Muebles'),
    ('decoracion', 'Decoración para el Hogar'),
    ('cocina', 'Cocina y Menaje'),
    ('herramientas', 'Herramientas y Construcción'),
    ('otros', 'Otros'),
    ]


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Electronica')
    image = models.ImageField(
        upload_to='products/', 
        blank=True,  # Permite dejarlo vacío en la base de datos
        null=True,   # Permite valores nulos en la base de datos
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])])
    
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    payments = [
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('efectivo', 'Efectivo'),
        ('paypal', 'PayPal'),
        ('cripto', 'Criptomoneda'),
    ]
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # 🔹 Asegúrate de que este campo existe
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # 🔹 Asegúrate de que este campo existe
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    payment = models.CharField(max_length=10, choices=payments, default='tarjeta')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=Customer.payments,default='tarjeta')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendiente')
    address = models.CharField(max_length=100)
    phone= models.TextField(max_length=10)

    def __str__(self):
        return f"Orden de {self.customer.user.username} - {self.product.name}"