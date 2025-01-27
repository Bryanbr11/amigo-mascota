# Generated by Django 5.1.4 on 2024-12-18 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='diagnostico_ia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='peso',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='signos_clinicos',
            field=models.TextField(default='No especificado'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='sintomas',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='motivo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
