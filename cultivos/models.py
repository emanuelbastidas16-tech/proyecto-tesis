from django.db import models

class Cultivo(models.Model):
    NOMBRE_OPCIONES = [
        ('maiz', 'Maíz'),
        ('platano', 'Plátano'),
        ('arroz', 'Arroz'),
        ('cafe', 'Café'),
        ('yuca', 'Yuca'),
    ]
    nombre = models.CharField(max_length=50, choices=NOMBRE_OPCIONES, unique=True)
    descripcion = models.TextField()
    ciclo_dias = models.IntegerField(help_text="Días promedio desde siembra a cosecha")
    rendimiento_min_m2 = models.FloatField(help_text="Kg mínimos por metro cuadrado")
    rendimiento_max_m2 = models.FloatField(help_text="Kg máximos por metro cuadrado")

    def __str__(self):
        return self.get_nombre_display()

# ESTE ES EL QUE FALTA O TIENE ERROR DE NOMBRE:
class Planificacion(models.Model):
    ESTADOS_VENEZUELA = [
        ('amazonas', 'Amazonas'), ('anzoategui', 'Anzoátegui'), ('apure', 'Apure'),
        ('aragua', 'Aragua'), ('barinas', 'Barinas'), ('bolivar', 'Bolívar'),
        ('carabobo', 'Carabobo'), ('cojedes', 'Cojedes'), ('delta_amacuro', 'Delta Amacuro'),
        ('distrito_capital', 'Distrito Capital'), ('falcon', 'Falcón'), ('guarico', 'Guárico'),
        ('lara', 'Lara'), ('merida', 'Mérida'), ('miranda', 'Miranda'),
        ('monagas', 'Monagas'), ('nueva_esparta', 'Nueva Esparta'), ('portuguesa', 'Portuguesa'),
        ('sucre', 'Sucre'), ('tachira', 'Táchira'), ('trujillo', 'Trujillo'),
        ('vargas', 'La Guaira'), ('yaracuy', 'Yaracuy'), ('zulia', 'Zulia'),
    ]
    
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_siembra = models.DateField()
    area_m2 = models.FloatField()
    estado = models.CharField(max_length=50, choices=ESTADOS_VENEZUELA, default='barinas')
    # Añadimos el tipo de suelo de una vez para la siguiente mejora
    TIPO_SUELO = [
        ('optimo', 'Suelo Suelto / Muy Fértil'),
        ('medio', 'Suelo Normal'),
        ('dificil', 'Suelo Duro / Arcilloso'),
    ]
    suelo = models.CharField(max_length=20, choices=TIPO_SUELO, default='medio')

class PasoCultivo(models.Model):
    cultivo = models.ForeignKey(Cultivo, related_name='pasos', on_delete=models.CASCADE)
    orden = models.IntegerField()
    titulo = models.CharField(max_length=200)
    instrucciones = models.TextField()

    class Meta:
        ordering = ['orden']