from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_leitores, name='lista_leitores'),
    path('imprimir-etiqueta/visualizar/<int:numero_leitor>/', views.visualizar_etiqueta, name='visualizar_etiqueta'),
    path('imprimir-etiqueta/<int:numero_leitor>/', views.imprimir_etiqueta, name='imprimir_etiqueta'),
    path('leitores/', views.lista_leitores, name='lista_leitores'),
    path('imprimir-etiquetas/', views.imprimir_etiquetas, name='imprimir_etiquetas'),
    path('visualizar-impressao/', views.visualizar_impressao, name='visualizar_impressao'),
    path('confirmar-impressao/', views.confirmar_impressao, name='confirmar_impressao'),
    path('remover-numero/<int:numero>/', views.remover_numero, name='remover_numero'),
    path('visualizar-etiqueta/<int:numero_leitor>/', views.visualizar_etiqueta, name='visualizar_etiqueta'),
]