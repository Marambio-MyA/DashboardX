from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=255)
    cantidad_disponible = models.IntegerField()
    precio_unitario = models.IntegerField()
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(cantidad_disponible__gte=0),
                name='cantidad_no_negativa'
            ),
            models.CheckConstraint(
                check=models.Q(precio_unitario__gte=0),
                name='precio_no_negativo'
            )
        ]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
