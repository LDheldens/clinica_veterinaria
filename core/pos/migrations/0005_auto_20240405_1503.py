# Generated by Django 3.2.2 on 2024-04-05 20:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_auto_20240405_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cita',
            name='descipcion',
        ),
        migrations.AddField(
            model_name='cita',
            name='descripcion',
            field=models.TextField(null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='asunto',
            field=models.TextField(verbose_name='Asunto'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_cita',
            field=models.DateField(verbose_name='Fecha de la cita'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='hora_cita',
            field=models.TimeField(verbose_name='Hora de la cita'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.datetime(2024, 4, 5, 20, 3, 46, 772338, tzinfo=utc)),
        ),
    ]
