# Generated by Django 4.2.9 on 2024-12-19 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('CREATE', 'Creación'), ('UPDATE', 'Actualización'), ('DELETE', 'Eliminación'), ('LOGIN', 'Inicio de sesión'), ('LOGOUT', 'Cierre de sesión')], max_length=20)),
                ('details', models.TextField()),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'activity_logs_activitylog',
            },
        ),
    ]
