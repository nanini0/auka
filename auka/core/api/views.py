from rest_framework import viewsets
from core.models import Producto,Categoria
from .serializers import ProductoSerializer,CategoriaSerializer,CategoriaConProductosSerializer
    
class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    
    serializer_class = ProductoSerializer
    
    def get_queryset(self):
        # 1. CORRECCIÓN: Asignamos el resultado a la variable 'queryset'
        queryset = Producto.objects.filter(stock=True).prefetch_related('ofertas', 'categorias')
        
        # 2. Capturamos el parámetro
        nombre_cat = self.request.query_params.get('categoria')
        
       
        if nombre_cat:
            # Ahora sí, 'queryset' existe, así que podemos filtrarlo más
            queryset = queryset.filter(categorias__nombre_cat__icontains=nombre_cat)

        
        return queryset
    

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    # 1. Optimizamos la consulta: "Trae categorías Y PRE-CARGA sus productos"
        queryset = Categoria.objects.prefetch_related('productos').all()
    
    # 2. Usamos el nuevo serializer que incluye la lista anidada
        serializer_class = CategoriaConProductosSerializer