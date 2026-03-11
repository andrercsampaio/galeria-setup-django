from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from .models import Carro, Pista, Setup

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    carros = Carro.objects.filter(publicado=True)
    pistas = Pista.objects.all()
    context = {'carros': carros, 'pistas': pistas}
    return render(request, 'catalogo/index.html', context)


def detalhe_carro(request, carro_id):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    carro = get_object_or_404(Carro, pk=carro_id)
    pistas_disponiveis = Pista.objects.filter(setups__carro=carro).distinct()
    return render(request, 'catalogo/detalhe_carro.html', {
        'carro': carro,
        'pistas': pistas_disponiveis
    })

def mostrar_todas_as_pistas(request):
    pistas = Pista.objects.annotate(total_setups=Count('setups'))
    return render(request, 'catalogo/todas_as_pistas.html', {'pistas': pistas})

def explorar_pista(request, pista_id):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    pista = get_object_or_404(Pista, pk=pista_id)
    carros_disponiveis = Carro.objects.filter(setups__pista=pista).distinct()
    return render(request, 'catalogo/explorar_pista.html', {
        'pista': pista,
        'carros': carros_disponiveis
    })

def setups_por_pista(request, carro_id, pista_id):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    carro = get_object_or_404(Carro, pk=carro_id)
    pista = get_object_or_404(Pista, pk=pista_id)
    setups = Setup.objects.filter(carro=carro, pista=pista)
    return render(request, 'catalogo/setup_por_pista.html', {
        'carro': carro,
        'pista': pista,
        'setups': setups
    })

def buscar(request):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    setups = Setup.objects.filter(carro__publicado=True).order_by('-data_criacao')
    if 'q' in request.GET:
        termo = request.GET['q']
        if termo:
            setups = setups.filter(carro__nome__icontains=termo) | setups.filter(pista__nome__icontains=termo)
    return render(request, 'catalogo/buscar.html', {'setups': setups, 'termo': request.GET.get('q', '')})