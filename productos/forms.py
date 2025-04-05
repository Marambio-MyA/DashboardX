from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad_disponible', 'precio_unitario', 'categoria']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'cantidad_disponible': forms.NumberInput(attrs={'min': 0}),
            'precio_unitario': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'cantidad_disponible': 'Cantidad Disponible',
            'precio_unitario': 'Precio Unitario',
            'categoria': 'Categoría'
        } 
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']