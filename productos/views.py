from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import logging
from .models import Producto
from .forms import ProductoForm

logger = logging.getLogger(__name__)

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        logger.info("Recibiendo POST para crear producto")
        form = ProductoForm(request.POST)
        if form.is_valid():
            logger.info("Formulario válido, intentando guardar")
            try:
                producto = form.save()
                logger.info(f"Producto guardado exitosamente: {producto.nombre}")
                messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
                return redirect('lista_productos')
            except Exception as e:
                logger.error(f"Error al guardar producto: {str(e)}")
                messages.error(request, f'Error al guardar el producto: {str(e)}')
        else:
            logger.error(f"Formulario inválido: {form.errors}")
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})
