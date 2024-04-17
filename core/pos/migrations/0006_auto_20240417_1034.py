# Generated by Django 3.2.2 on 2024-04-17 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0005_merge_0003_cirugia_0004_auto_20240415_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cirugia',
            name='firma_propietario',
            field=models.ImageField(upload_to='firmas/', verbose_name='Firma del propietario para el consentimiento de la cirugia'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='identificacion',
            field=models.CharField(max_length=150, verbose_name='Identificación de la mascota: FORMATO (SVT-1)'),
        ),
    ]