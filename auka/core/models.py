from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
# Create your models here.
 
class Categoria(models.Model):
    nombre_cat=models.CharField(max_length=40,
                                verbose_name='nombre')
    descripcion_cat= models.TextField(verbose_name='descipcion')
    
    def __str__(self):
        return self.nombre_cat
    

class Producto(models.Model):
    nombre_prod = models.CharField(max_length=60, verbose_name='producto')
    precio_prod = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descripcion_prod = models.TextField(verbose_name='descipcion')
    img_prod = models.ImageField(upload_to='producto/')
    beneficio_prod = models.CharField(max_length=200)
    # Nota: related_name='productos' en Categoria es redundante si ya lo defines aquí, 
    # pero como es M2M está bien.
    categorias = models.ManyToManyField(Categoria, related_name="productos", blank=True)
    stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_prod} (${self.precio_prod}) {self.stock}"
    
    @property
    def precio_actual(self):
        ahora = timezone.now()
        
        
        oferta_activa = self.ofertas.filter(
            activa=True,
            fecha_inicio__lte=ahora,
            fecha_fin__gte=ahora
        ).order_by('-porcentaje_descuento').first()
        
       
        if oferta_activa:
            descuento = (self.precio_prod * oferta_activa.porcentaje_descuento) / Decimal(100)
            return round(self.precio_prod - descuento, 2)
            
        return self.precio_prod      

    @property
    def tiene_descuento(self):
        return self.precio_actual < self.precio_prod
class Servicios(models.Model):
    nombre_serv=models.CharField(max_length=50,
                                 verbose_name='nombre')
    descripcion_serv=models.TextField()
    img_serv=models.ImageField(upload_to='servicio/')
    precio_serv=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0.00)])

    def __str__(self):
        return f"{self.nombre_serv} (${self.precio_serv})"


class ProductoDestacado(models.Model):
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name='destacados',
        verbose_name='Producto destacado'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, verbose_name='¿Activo?')
    orden = models.PositiveIntegerField(
        default=0,
        help_text='Orden de aparición (mayor número = más prioritario)'
    )
    
    class Meta:
        verbose_name = 'Producto destacado'
        verbose_name_plural = 'Productos destacados'
        ordering = ['-orden', '-fecha_creacion']
    
    def __str__(self):
        return f"Destacado: {self.producto.nombre_prod}"
    


class Oferta(models.Model):
    nombre = models.CharField(max_length=100,help_text="Ej:'Oferta de Invierno', 'Liquidación Final' ")
    productos = models.ManyToManyField('Producto',related_name='ofertas',blank=True)
    porcentaje_descuento = models.DecimalField(max_digits=5,decimal_places=2,help_text="Porcentaje de descuentos(ej: 15 para un 15%)")
    fecha_inicio = models.DateTimeField()
    fecha_fin= models.DateTimeField()
    activa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje_descuento}%)"
    class Meta:
        ordering = ['-fecha_fin']



class Blog(models.Model):
    titulo=models.CharField(max_length=250)
    contenido=models.TextField()
    fecha_publicacion=models.DateTimeField()
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última modificación"
    )
    activa=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} {self.activa}"
    class Meta:
        ordering = ['-fecha_publicacion']
        
