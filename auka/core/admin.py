from django.contrib import admin
from .models import Producto,Categoria,Oferta
# Register your models here.
admin.site.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria', 'stock']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock']

admin.site.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

admin.site.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'descuento', 'fecha_inicio', 'fecha_fin']
    list_filter = ['fecha_inicio', 'fecha_fin']