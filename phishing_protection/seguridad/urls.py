
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, CorreoElectricoViewSet, PhishingReporteViewSet, ConfiguracionSeguridadViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'correos', CorreoElectricoViewSet)
router.register(r'reportes', PhishingReporteViewSet)
router.register(r'configuraciones', ConfiguracionSeguridadViewSet)

urlpatterns = [
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('predecir/', views.predecir, name='predecir'),
    path('configuracion/<int:id_usuario>/', views.obtener_configuraciones, name='obtener_configuracion'),
]