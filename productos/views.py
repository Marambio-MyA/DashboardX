from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
import logging
from .models import Producto,Categoria
from .forms import ProductoForm, CategoriaForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


logger = logging.getLogger(__name__)

@login_required
def home(request):
    categorias = Categoria.objects.all()

    # Filtrado de productos
    productos = Producto.objects.all()

    search = request.GET.get('search')
    categoria_id = request.GET.get('categoria')
    stock = request.GET.get('stock')

    if search:
        productos = productos.filter(nombre__icontains=search)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if stock:
        productos = productos.filter(cantidad_disponible__gte=stock)

    context = {
        'productos': productos,
        'categorias': categorias,
    }

    return render(request, 'home.html', context)

@login_required
def lista_productos(request):
    nombre_busqueda = request.GET.get('nombre', '')
    categoria_filtro = request.GET.get('categoria', '')
    stock_filtro = request.GET.get('stock', '')

    productos = Producto.objects.all()

    if nombre_busqueda:
        productos = productos.filter(nombre__icontains=nombre_busqueda)

    if categoria_filtro:
        productos = productos.filter(categoria__id=categoria_filtro)

    if stock_filtro:
        if stock_filtro == 'agotado':
            productos = productos.filter(cantidad_disponible=0)
        elif stock_filtro == 'disponible':
            productos = productos.filter(cantidad_disponible__gt=0)

    categorias = Categoria.objects.all()  # Para mostrar en el filtro

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'categorias': categorias,
        'nombre_busqueda': nombre_busqueda,
        'categoria_filtro': categoria_filtro,
        'stock_filtro': stock_filtro
    })
    
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
                return redirect('home')
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
            return redirect('home')
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
        return redirect('home')
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

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/listar_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/crear_categoria.html', {'form': form})

@login_required
def editar_categoria(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    categoria.delete()
    return redirect('home')


def custom_logout(request):
    logout(request)
    return redirect('/login/?logout=1') 
