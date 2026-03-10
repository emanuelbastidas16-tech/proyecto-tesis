from django.shortcuts import render
from .models import Cultivo, Planificacion
from datetime import timedelta
import datetime

def calcular_siembra(request):
    resultado = None
    pasos = None
    mensaje_clima = ""
    
    if request.method == "POST":
        # 1. Capturar datos del formulario
        cultivo_id = request.POST.get('cultivo')
        area = float(request.POST.get('area'))
        fecha_inicio = request.POST.get('fecha')
        estado_seleccionado = request.POST.get('estado')
        tipo_suelo = request.POST.get('suelo')
        
        # 2. Obtener el objeto del cultivo de la base de datos
        obj_cultivo = Cultivo.objects.get(id=cultivo_id)
        
        # 3. Lógica de CLIMA (Ajuste de tiempo de cosecha)
        # Definimos estados donde el ciclo es más lento por el frío
        estados_frios = ['merida', 'tachira', 'trujillo']
        dias_base = obj_cultivo.ciclo_dias
        
        if estado_seleccionado in estados_frios:
            dias_finales = int(dias_base * 1.2) # 20% más de tiempo
            mensaje_clima = "Debido al clima templado/frío de tu estado, el cultivo tardará un poco más en estar listo."
        else:
            dias_finales = dias_base
            mensaje_clima = "El clima de tu estado permite un ciclo de crecimiento estándar."

        # 4. Calcular fecha exacta
        fecha_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_cosecha = fecha_dt + timedelta(days=dias_finales)
        
        # 5. Lógica de SUELO (Ajuste de producción en Kg)
        # Multiplicadores de eficiencia según el suelo
        ajustes = {'optimo': 1.0, 'medio': 0.8, 'dificil': 0.6}
        factor_suelo = ajustes.get(tipo_suelo, 0.8)
        
        prod_min = area * obj_cultivo.rendimiento_min_m2 * factor_suelo
        prod_max = area * obj_cultivo.rendimiento_max_m2 * factor_suelo
        
        # 6. Obtener los pasos de este cultivo (ordenados)
        pasos = obj_cultivo.pasos.all()
        
        resultado = {
            'cultivo': obj_cultivo.get_nombre_display(),
            'fecha_cosecha': fecha_cosecha,
            'min': round(prod_min, 2), # Redondeamos a 2 decimales
            'max': round(prod_max, 2),
            'mensaje': mensaje_clima,
            'estado': estado_seleccionado.capitalize()
        }

    # Datos que siempre se envían a la página (para llenar los select)
    lista_cultivos = Cultivo.objects.all()
    # Enviamos la lista de estados que definimos en el Modelo
    lista_estados = Planificacion.ESTADOS_VENEZUELA 
    
    contexto = {
        'cultivos': lista_cultivos, 
        'lista_estados': lista_estados,
        'resultado': resultado,
        'pasos': pasos
    }
    
    return render(request, 'cultivos/calculadora.html', contexto)