from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categoria, Producto

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto)