from django.shortcuts import render

from rest_framework import viewsets
from .models import Usuario, CorreoElectrico, PhishingReporte, ConfiguracionSeguridad
from .serializers import UsuarioSerializer, CorreoElectricoSerializer, PhishingReporteSerializer, ConfiguracionSeguridadSerializer
from django.http import HttpResponse
from django.http import JsonResponse
import pickle
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ConfiguracionSeguridadSerializer

def home(request):
    return HttpResponse("Bienvenido al backend de Phishing Protection.")

def usuario_list(request):
    usuarios = Usuario.objects.all()  # Consulta todos los usuarios
    usuarios_data = list(usuarios.values())  # Convierte el queryset en una lista de diccionarios
    return JsonResponse(usuarios_data, safe=False)  # Devuelve los datos como JSON

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class CorreoElectricoViewSet(viewsets.ModelViewSet):
    queryset = CorreoElectrico.objects.all()
    serializer_class = CorreoElectricoSerializer

class PhishingReporteViewSet(viewsets.ModelViewSet):
    queryset = PhishingReporte.objects.all()
    serializer_class = PhishingReporteSerializer

class ConfiguracionSeguridadViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionSeguridad.objects.all()
    serializer_class = ConfiguracionSeguridadSerializer

# Cargar el modelo y el vectorizador (esto puede hacerse fuera de la vista si no cambia durante las solicitudes)
with open('models/modelo_spam.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('models/vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Función para predecir si un correo es spam o no
def predecir_spam(correo_texto):
    correo_transformado = vectorizer.transform([correo_texto])
    prediccion = model.predict(correo_transformado)
    return "Malicioso" if prediccion[0] == 1 else "Legítimo"

# Vista para recibir correo y devolver la predicción
@csrf_exempt
def predecir(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                # Leer los datos JSON del cuerpo de la solicitud
                data = json.loads(request.body)
                correo_texto = data.get('contenido')

                if correo_texto:
                    resultado = predecir_spam(correo_texto)
                    return JsonResponse({'resultado': resultado})
                else:
                    return JsonResponse({'error': 'No se proporcionó contenido en el correo'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Error al procesar el JSON'}, status=400)
        else:
            return JsonResponse({'error': 'Tipo de contenido no permitido. Usa application/json.'}, status=415)

    # Si la solicitud no es POST, respondemos con un error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_configuraciones(request, id_usuario):
    try:
        configuracion = ConfiguracionSeguridad.objects.get(id_usuario=id_usuario)
        data = {
            'nivel_seguridad': configuracion.nivel_seguridad,
            'notificacion': configuracion.notificacion
        }
        return JsonResponse(data, status=200)
    except ConfiguracionSeguridad.DoesNotExist:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=404)


@api_view(['GET'])
def obtener_configuraciones(request, id_usuario):
    try:
        configuracion = ConfiguracionSeguridad.objects.get(id_usuario=id_usuario)
        serializer = ConfiguracionSeguridadSerializer(configuracion)
        return Response(serializer.data)
    except ConfiguracionSeguridad.DoesNotExist:
        return Response({'error': 'Configuración no encontrada'}, status=404)