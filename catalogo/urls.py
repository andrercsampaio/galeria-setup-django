from django.urls import path
from . import views 

urlpatterns = [
    # --- index ---
    path('', views.index, name='index'),

    # --- busca ---
    path('buscar/', views.buscar, name='buscar'),

    # --- pistas ---
    path('pistas/', views.mostrar_todas_as_pistas, name='todas_as_pistas'),
    path('pista/<int:pista_id>/', views.explorar_pista, name='explorar_pista'),

    # --- carros ---
    path('carros/', views.mostrar_todas_os_carros, name='todos_os_carros'),
    path('carro/<int:carro_id>/', views.detalhe_carro, name='detalhe_carro'),
    path('carro/<int:carro_id>/pista/<int:pista_id>/', views.setups_por_pista, name='setups_por_pista'),

    # --- MINHA GARAGEM (PRIVADO) ---
    path('meus_setups/', views.meus_setups, name='meus_setups'),
    
    # Rota Única para Criar: Mostra o formulário E salva os dados
    path('meus_setups/novo/', views.novo_setup_privado, name='novo_setup_privado'),
    
    # Rotas para Editar e Eliminar (Precisam do ID do setup)
    path('meus_setups/editar/<int:setup_id>/', views.editar_setup_privado, name='editar_setup_privado'),
    path('meus_setups/deletar/<int:setup_id>/', views.deletar_setup_privado, name='deletar_setup_privado'),

    # --- COMUNIDADE (PÚBLICO) ---
    path('setups_comunidade/', views.setups_comunidade, name='setups_comunidade'),
    path('setups_comunidade_pesquisa/', views.setups_comunidade_pesquisa, name='setups_comunidade_pesquisa'),
]