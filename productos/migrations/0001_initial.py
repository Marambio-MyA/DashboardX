# Generated by Django 5.2 on 2025-04-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('cantidad_disponible', models.IntegerField()),
                ('precio_unitario', models.IntegerField()),
                ('categoria', models.CharField(max_length=50)),
            ],
            options={
                'constraints': [models.CheckConstraint(check=models.Q(('cantidad_disponible__gte', 0)), name='cantidad_no_negativa'), models.CheckConstraint(check=models.Q(('precio_unitario__gte', 0)), name='precio_no_negativo')],
            },
        ),
    ]