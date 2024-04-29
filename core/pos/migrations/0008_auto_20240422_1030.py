# Generated by Django 3.2.2 on 2024-04-22 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0007_merge_0003_auto_20240419_1358_0006_paciente_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='edad',
            field=models.IntegerField(blank=True, null=True, verbose_name='Edad'),
        ),
        migrations.CreateModel(
            name='HistorialClinico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.paciente', verbose_name='Mascota')),
            ],
        ),
    ]