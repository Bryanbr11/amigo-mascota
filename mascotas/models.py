from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

class Especie(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'especie'
        verbose_name_plural = 'especies'

class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
        ('CONEJO', 'Conejo'),
        ('HAMSTER', 'Hámster'),
        ('AVE', 'Ave'),
        ('PEZ', 'Pez'),
        ('REPTIL', 'Reptil'),
        ('OTRO', 'Otro'),
    ]

    RAZAS_POR_ESPECIE = {
        'PERRO': [
            ('LABRADOR', 'Labrador Retriever'),
            ('PASTOR_ALEMAN', 'Pastor Alemán'),
            ('BULLDOG', 'Bulldog'),
            ('GOLDEN', 'Golden Retriever'),
            ('CHIHUAHUA', 'Chihuahua'),
            ('POODLE', 'Poodle'),
            ('ROTTWEILER', 'Rottweiler'),
            ('YORKSHIRE', 'Yorkshire Terrier'),
            ('BOXER', 'Boxer'),
            ('OTRO', 'Otro'),
        ],
        'GATO': [
            ('PERSA', 'Persa'),
            ('SIAMES', 'Siamés'),
            ('ANGORA', 'Angora'),
            ('BENGALI', 'Bengalí'),
            ('MAINE_COON', 'Maine Coon'),
            ('BRITISH', 'British Shorthair'),
            ('SPHYNX', 'Sphynx'),
            ('RAGDOLL', 'Ragdoll'),
            ('OTRO', 'Otro'),
        ],
        'CONEJO': [
            ('HOLANDES', 'Holandés'),
            ('CABEZA_LEON', 'Cabeza de León'),
            ('ANGORA', 'Angora'),
            ('REX', 'Rex'),
            ('OTRO', 'Otro'),
        ],
        'HAMSTER': [
            ('SIRIO', 'Sirio'),
            ('RUSO', 'Ruso'),
            ('ROBOROVSKI', 'Roborovski'),
            ('CHINO', 'Chino'),
            ('OTRO', 'Otro'),
        ],
        'AVE': [
            ('CANARIO', 'Canario'),
            ('PERIQUITO', 'Periquito'),
            ('AGAPORNIS', 'Agapornis'),
            ('CACATUA', 'Cacatúa'),
            ('OTRO', 'Otro'),
        ],
        'PEZ': [
            ('BETA', 'Beta'),
            ('GOLDFISH', 'Goldfish'),
            ('GUPPY', 'Guppy'),
            ('TETRA', 'Tetra'),
            ('OTRO', 'Otro'),
        ],
        'REPTIL': [
            ('IGUANA', 'Iguana'),
            ('GECKO', 'Gecko'),
            ('TORTUGA', 'Tortuga'),
            ('DRAGON_BARBUDO', 'Dragón Barbudo'),
            ('OTRO', 'Otro'),
        ],
        'OTRO': [
            ('OTRO', 'Otro'),
        ],
    }

    nombre = models.CharField(max_length=100)
    especie = models.CharField(
        max_length=20,
        choices=ESPECIE_CHOICES,
        default='PERRO'
    )
    raza = models.CharField(
        max_length=50,
        default='OTRO'
    )
    fecha_nacimiento = models.DateField()
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Peso en kilogramos"
    )
    foto = models.ImageField(
        upload_to='mascotas/',
        null=True,
        blank=True
    )
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mascotas_propietario'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_especie_display()} ({self.raza})"

    class Meta:
        verbose_name = 'mascota'
        verbose_name_plural = 'mascotas'
        ordering = ['-fecha_registro']

    @property
    def edad(self):
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def get_razas_for_especie(self):
        return dict(self.RAZAS_POR_ESPECIE.get(self.especie, [('OTRO', 'Otro')]))

    def clean(self):
        super().clean()
        if self.fecha_nacimiento and self.fecha_nacimiento > date.today():
            raise ValidationError({
                'fecha_nacimiento': _("La fecha de nacimiento no puede ser en el futuro.")
            })