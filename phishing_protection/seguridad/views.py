from django.shortcuts import render

from rest_framework import viewsets
from .models import Usuario, CorreoElectrico, PhishingReporte, ConfiguracionSeguridad
from .serializers import UsuarioSerializer, CorreoElectricoSerializer, PhishingReporteSerializer, ConfiguracionSeguridadSerializer
from django.http import HttpResponse
from django.http import JsonResponse

def home(request):
    return HttpResponse("Bienvenido al backend de Phishing Protection.")

def usuario_list(request):
    return JsonResponse({"mensaje": "Lista de usuarios (ejemplo)."})

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
