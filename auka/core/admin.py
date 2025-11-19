from django.contrib import admin
from django.utils.html import format_html # Necesario para mostrar imágenes
from .models import Producto, Categoria, Oferta, ProductoDestacado

# 1. CONFIGURACIÓN DE CATEGORÍA
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_cat', 'descripcion_corta'] # Campos a mostrar
    search_fields = ['nombre_cat'] # Barra de búsqueda
    list_display_links = ['nombre_cat'] # Click para editar

    # Truco: Función para cortar descripciones largas
    def descripcion_corta(self, obj):
        return obj.descripcion_cat[:50] + "..." if len(obj.descripcion_cat) > 50 else obj.descripcion_cat
    descripcion_corta.short_description = "Descripción"

# 2. CONFIGURACIÓN DE PRODUCTO (¡La más importante!)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Mostramos imagen pequeña, nombre, precio original, precio calculado y stock
    list_display = ['imagen_preview', 'nombre_prod', 'precio_prod', 'ver_precio_actual', 'stock', 'mostrar_categorias']
    
    # Filtros laterales
    list_filter = ['stock', 'categorias'] 
    
    # Buscador (busca por nombre o descripción)
    search_fields = ['nombre_prod', 'descripcion_prod']
    
    # Edición rápida desde la lista (sin entrar al producto)
    list_editable = ['stock', 'precio_prod']
    
    # Campos de solo lectura al entrar a editar
    readonly_fields = ['ver_precio_actual']

    # --- FUNCIONES PERSONALIZADAS ---

    # A. Función para ver la imagen
    def imagen_preview(self, obj):
        if obj.img_prod:
            # Creamos etiqueta HTML <img> segura
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.img_prod.url)
        return "Sin imagen"
    imagen_preview.short_description = "Img"

    # B. Función para ver el precio calculado (El @property del modelo)
    def ver_precio_actual(self, obj):
        precio = obj.precio_actual
        if obj.tiene_descuento:
            # Si tiene descuento, lo pintamos de verde y negrita
            return format_html('<span style="color: green; font-weight: bold;">${}</span>', precio)
        return f"${precio}"
    ver_precio_actual.short_description = "Precio Final"

    # C. Función para mostrar ManyToMany (Categorías)
    # Django no deja mostrar campos M2M directos en list_display, hay que iterarlos
    def mostrar_categorias(self, obj):
        # Toma todas las categorías y las une con comas
        return ", ".join([c.nombre_cat for c in obj.categorias.all()])
    mostrar_categorias.short_description = "Categorías"

# 3. CONFIGURACIÓN DE OFERTA
@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'porcentaje_descuento', 'fecha_inicio', 'fecha_fin', 'estado_oferta', 'activa']
    list_filter = ['activa', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_inicio' # Navegación por fechas arriba

    # Función visual para ver si está vigente
    def estado_oferta(self, obj):
        from django.utils import timezone
        ahora = timezone.now()
        if obj.activa and obj.fecha_inicio <= ahora <= obj.fecha_fin:
             return format_html('<span style="color: green;">🟢 Vigente</span>')
        return format_html('<span style="color: red;">🔴 No vigente</span>')
    estado_oferta.short_description = "Estado"

# 4. CONFIGURACIÓN DE DESTACADOS
@admin.register(ProductoDestacado)
class ProductoDestacadoAdmin(admin.ModelAdmin):
    # 1. El orden de las columnas
    list_display = ['orden', 'get_producto_nombre', 'activo', 'fecha_creacion']
    
    # 2. LO QUE FALTABA: Le decimos que el ENLACE para entrar sea el nombre, NO el orden.
    list_display_links = ['get_producto_nombre'] 
    
    # 3. Ahora 'orden' es libre para ser editable
    list_editable = ['orden', 'activo'] 
    
    list_filter = ['activo']
    ordering = ['orden'] 

    def get_producto_nombre(self, obj):
        return obj.producto.nombre_prod
    get_producto_nombre.short_description = "Producto"