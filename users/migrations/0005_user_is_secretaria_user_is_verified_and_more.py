# Generated by Django 4.2.9 on 2024-12-19 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_secretaria',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_veterinario',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='license_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
