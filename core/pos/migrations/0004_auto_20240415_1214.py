# Generated by Django 3.2.2 on 2024-04-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_alter_paciente_unidad_edad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='identificacion',
            field=models.CharField(max_length=150, verbose_name='Identificación de la mascota'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='unidad_edad',
            field=models.CharField(choices=[('año(s)', 'Año(s)'), ('mes(es)', 'Mes(es)')], default='año(s)', max_length=20, verbose_name='Unidad de edad'),
        ),
    ]