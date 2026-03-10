from django.contrib import admin
# Importamos tus modelos desde el archivo models.py de esta misma carpeta
from .models import Cultivo, Planificacion, PasoCultivo

# Esto le dice a Django: "Muestra estas tablas en el panel de administrador"
admin.site.register(Cultivo)
admin.site.register(Planificacion)
admin.site.register(PasoCultivo)
