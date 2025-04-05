from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import logging
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


logger = logging.getLogger(__name__)

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

@login_required
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

@login_required
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

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})

@login_required
def reporte_inventario_pdf(request):
    # Crear la respuesta como un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Datos del inventario
    productos = Producto.objects.all()
    total_cantidad = sum(p.cantidad_disponible for p in productos)
    valor_total = sum(p.cantidad_disponible * p.precio_unitario for p in productos)
    productos_agotados = productos.filter(cantidad_disponible=0)

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Reporte de Inventario")
    y -= 30

    # Total de productos en inventario y valor total
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Total de productos en inventario: {total_cantidad}")
    y -= 20
    p.drawString(50, y, f"Valor total del inventario: ${valor_total:,.2f}")
    y -= 40

    # Productos agotados
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Productos agotados:")
    y -= 20
    p.setFont("Helvetica", 11)

    if productos_agotados.exists():
        for prod in productos_agotados:
            if y < 50:
                p.showPage()
                y = height - 50
            p.drawString(60, y, f"- {prod.nombre} (Cantidad: {prod.cantidad_disponible})")
            y -= 15
    else:
        p.drawString(60, y, "No hay productos agotados.")
        y -= 15
        
    y -= 25
    # Lista completa de productos
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Lista completa de productos:")
    y -= 20
    p.setFont("Helvetica", 12)

    for producto in productos:
        p.drawString(60, y, f"- {producto.nombre}: {producto.cantidad_disponible} disponibles")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    # Finalizar PDF
    p.showPage()
    p.save()
    return response