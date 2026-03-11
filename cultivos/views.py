from django.shortcuts import render
from .models import Cultivo, Planificacion
from datetime import timedelta
import datetime

def calcular_siembra(request):
    resultado = None
    pasos = None
    
    # 1. Diccionario de Regiones de Venezuela (Base de Conocimiento)
    regiones_vzla = {
        'andina': ['merida', 'tachira', 'trujillo'],
        'llanos': ['barinas', 'portuguesa', 'guarico', 'apure', 'cojedes'],
        'centro_occidente': ['lara', 'falcon', 'yaracuy'],
        'oriente': ['monagas', 'anzoategui', 'sucre', 'bolivar', 'delta_amacuro', 'amazonas'],
        'central': ['aragua', 'carabobo', 'miranda', 'vargas', 'distrito_capital'],
        'insular': ['nueva_esparta', 'zulia']
    }

    # 2. Matriz de Recomendaciones Inteligentes
    recomendaciones_expertas = {
        'andina': {
            'optimo': "Zona alta y fértil: Ideal para Papa, Zanahoria, Fresa o Ajo.",
            'medio': "Clima frío: Recomendamos hortalizas de hoja como Lechuga o Brócoli.",
            'dificil': "Suelo pesado en montaña: Sugerimos Pastos de altura o Trigo."
        },
        'llanos': {
            'optimo': "Corazón agrícola: Maíz Blanco/Amarillo o Girasol son excelentes.",
            'medio': "Zona llanera estándar: Recomendamos Sorgo, Caraotas o Yuca.",
            'dificil': "Suelo arcilloso (estero): Ideal para Arroz o Caña de Azúcar."
        },
        'centro_occidente': {
            'optimo': "Suelo fértil y seco: Ideal para Cebolla, Pimentón o Melón.",
            'medio': "Clima semi-árido: Recomendamos Tomate, Piña o Sisal.",
            'dificil': "Suelo árido/duro: Considera Sábila (Aloe Vera) o Leguminosas resistentes."
        },
        'oriente': {
            'optimo': "Tierras bajas fértiles: Excelente para Palma Aceitera o Cacao.",
            'medio': "Sabanas orientales: Recomendamos Maní, Yuca o Cítricos.",
            'dificil': "Suelos ácidos/pesados: Sugerimos Pino caribe o pastizales."
        },
        'central': {
            'optimo': "Valles fértiles: Ideales para Tabaco, Frutales o Caña de Azúcar.",
            'medio': "Zona central: Recomendamos Hortalizas de ciclo corto (Ají, Cebollín).",
            'dificil': "Laderas/Suelo duro: Considera Café (zonas altas) o Leguminosas."
        },
        'insular': {
            'optimo': "Zona costera cálida: Ideal para Plátano, Cambur o Coco.",
            'medio': "Clima caliente: Recomendamos Patilla, Melón o Ají Dulce.",
            'dificil': "Suelo salino/duro: Sugerimos Palmeras o plantas resistentes al calor."
        }
    }

    if request.method == "POST":
        # Captura de datos del formulario
        cultivo_id = request.POST.get('cultivo')
        area = float(request.POST.get('area'))
        fecha_inicio = request.POST.get('fecha')
        estado_sel = request.POST.get('estado')
        suelo_sel = request.POST.get('suelo')

        # Obtener el cultivo seleccionado
        obj_cultivo = Cultivo.objects.get(id=cultivo_id)

        # A. DETERMINAR REGIÓN
        region_actual = 'desconocida'
        for reg, estados in regiones_vzla.items():
            if estado_sel in estados:
                region_actual = reg
                break

        # B. OBTENER RECOMENDACIÓN DEL SISTEMA EXPERTO
        msj_asesoria = recomendaciones_expertas.get(region_actual, {}).get(suelo_sel, "Consulte a un agrónomo local.")

        # C. LÓGICA DE TIEMPO (Clima)
        # Los estados andinos tardan un 20% más por el frío
        factor_clima = 1.2 if region_actual == 'andina' else 1.0
        dias_finales = int(obj_cultivo.ciclo_dias * factor_clima)
        
        fecha_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_cosecha = fecha_dt + timedelta(days=dias_finales)

        # D. LÓGICA DE PRODUCCIÓN (Suelo)
        ajustes_suelo = {'optimo': 1.0, 'medio': 0.8, 'dificil': 0.6}
        factor_suelo = ajustes_suelo.get(suelo_sel, 0.8)
        
        prod_min = area * obj_cultivo.rendimiento_min_m2 * factor_suelo
        prod_max = area * obj_cultivo.rendimiento_max_m2 * factor_suelo

        # E. PASOS DEL CULTIVO
        pasos = obj_cultivo.pasos.all()

        resultado = {
            'cultivo': obj_cultivo.get_nombre_display(),
            'fecha_cosecha': fecha_cosecha,
            'min': round(prod_min, 2),
            'max': round(prod_max, 2),
            'estado': estado_sel.replace('_', ' ').capitalize(),
            'asesoria': msj_asesoria
        }

    # Datos para los selectores del formulario
    contexto = {
        'cultivos': Cultivo.objects.all(),
        'lista_estados': Planificacion.ESTADOS_VENEZUELA,
        'resultado': resultado,
        'pasos': pasos
    }
    
    return render(request, 'cultivos/calculadora.html', contexto)