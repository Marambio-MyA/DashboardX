from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad_disponible = models.IntegerField()
    precio_unitario = models.IntegerField()
    categoria = models.CharField(max_length=50)

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
