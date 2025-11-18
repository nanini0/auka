
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# OJO con la importación: como estás dentro de 'core', importamos desde .views
from .views import ProductoViewSet
#CategoriaViewSet 

# 1. Creamos el Router
router = DefaultRouter()

# 2. Registramos las rutas
# Esto crea: /productos/ y /categorias/
router.register(r'productos', ProductoViewSet, basename='producto')

#router.register(r'categorias', CategoriaViewSet, basename='categoria')

# 3. Definimos urlpatterns
urlpatterns = [
    # Incluimos las URLs generadas por el router
    path('', include(router.urls)),
]