from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar/', views.buscar, name='buscar'),
    path('pistas/', views.mostrar_todas_as_pistas, name='todas_as_pistas'),
    path('carros/', views.mostrar_todas_os_carros, name='todos_os_carros'),
    path('pista/<int:pista_id>/', views.explorar_pista, name='explorar_pista'),
    path('carro/<int:carro_id>/', views.detalhe_carro, name='detalhe_carro'),
    path('carro/<int:carro_id>/pista/<int:pista_id>/', views.setups_por_pista, name='setups_por_pista'),
    path('meus_setups', views.meus_setups, name = 'meus_setups'),
    path('setups_comunidade', views.setups_comunidade, name='setups_comunidade'),
    path('setups_comunidade_pesquisa', views.setups_comunidade_pesquisa, name='setups_comunidade_pesquisa')
]