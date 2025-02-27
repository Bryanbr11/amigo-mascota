# Generated by Django 5.1.4 on 2024-12-17 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('raza', models.CharField(blank=True, max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('peso', models.FloatField(help_text='Peso en kilogramos')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='mascotas/')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mascotas', to='mascotas.especie')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mascotas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
