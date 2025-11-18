from rest_framework import viewsets
from core.models import Producto
from .serializers import ProductoSerializer
    
class ProductoViewSet(viewsets.ModelViewSet):
    
    serializer_class = ProductoSerializer
    
    def get_queryset(sefl):
        return Producto.objects.filter(stock=True).prefetch_related('ofertas', 'categorias').all()