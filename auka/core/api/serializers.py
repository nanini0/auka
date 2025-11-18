from rest_framework import serializers
from ..models import Producto, Categoria, Oferta

class CategoriaSerializer(serializers.ModelSerializer):
   class Meta:
        model = Categoria
        fields = ['id','nombre_cat', 'descripcion_cat']
        
class ProductoSerializer(serializers.ModelSerializer):
    precio_actual = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tiene_descuento = serializers.BooleanField(read_only=True)
    
    categorias = CategoriaSerializer(many=True, read_only=True)
    class Meta:
        model=Producto
        fields = [
            'id', 
            'nombre_prod', 
            'precio_prod',     
            'precio_actual',   
            'tiene_descuento', 
            'img_prod', 
            'stock',
            'categorias'
        ]