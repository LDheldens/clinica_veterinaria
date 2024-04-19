# Generated by Django 3.2.2 on 2024-04-19 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='edad',
            field=models.IntegerField(blank=True, null=True, verbose_name='Unidad de edad'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='fecha_nacimiento_value',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='unidad_edad',
            field=models.CharField(choices=[('año(s)', 'Año(s)'), ('mes(es)', 'Mes(es)')], default='año(s)', max_length=10, verbose_name='Unidad de edad'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='fecha_nacimiento',
            field=models.BooleanField(default=False, verbose_name='¿Conoces la fecha de nacimiento de tu mascota?'),
        ),
    ]