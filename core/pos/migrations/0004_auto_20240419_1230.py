# Generated by Django 3.2.2 on 2024-04-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_auto_20240419_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico',
            name='frecuencia_cardiaca',
            field=models.IntegerField(null=True, verbose_name='Frecuencia Cardíaca'),
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='frecuencia_respiratoria',
            field=models.IntegerField(null=True, verbose_name='Frecuencia Respiratoria'),
        ),
    ]