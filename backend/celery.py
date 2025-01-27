import os
from celery import Celery

# Establecer la configuración de Django por defecto para celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Usar la configuración de Django para celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar las tareas de todas las aplicaciones Django registradas
app.autodiscover_tasks()

# Configuración para evitar el warning
app.conf.broker_connection_retry_on_startup = True 