from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar/', views.buscar, name='buscar'),
    path('pistas/', views.mostrar_todas_as_pistas, name='todas_as_pistas'),
    path('pista/<int:pista_id>/', views.explorar_pista, name='explorar_pista'),
    path('carro/<int:carro_id>/', views.detalhe_carro, name='detalhe_carro'),
    path('carro/<int:carro_id>/pista/<int:pista_id>/', views.setups_por_pista, name='setups_por_pista'),
]