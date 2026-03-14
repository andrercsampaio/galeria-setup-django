from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from .models import Carro, Pista, SetupPublico, Setup
from catalogo.forms import SetupForm



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
    pistas_disponiveis = Pista.objects.filter(setups_privados__carro=carro).distinct()
    return render(request, 'catalogo/detalhe_carro.html', {
        'carro': carro,
        'pistas': pistas_disponiveis
    })


def mostrar_todas_as_pistas(request):
    pistas = Pista.objects.all()
    return render(request, 'catalogo/todas_as_pistas.html', {'pistas': pistas})


def mostrar_todas_os_carros(request):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    carros = Carro.objects.filter(publicado=True)
    return render(request, 'catalogo/todos_os carros.html', {'carros':carros})


def explorar_pista(request, pista_id):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    pista = get_object_or_404(Pista, pk=pista_id)
    carros_disponiveis = Carro.objects.all()
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
    setups = SetupPublico.objects.filter(carro__publicado=True).order_by('-data_criacao')
    if 'q' in request.GET:
        termo = request.GET['q']
        if termo:
            setups = setups.filter(carro__nome__icontains=termo) | setups.filter(pista__nome__icontains=termo)
    return render(request, 'catalogo/buscar.html', {'setups': setups, 'termo': request.GET.get('q', '')})


def meus_setups(request):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    
    setups = Setup.objects.filter(usuario=request.user).order_by('-data_criacao')
    carros = Carro.objects.all()
    pistas = Pista.objects.all()


    return render(request, 'catalogo/meus_setups.html', {
        'carros': carros,
        'pistas': pistas,
        'setups': setups
    })


def novo_setup_privado(request):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')

    if request.method == 'POST':
        form = SetupForm(request.POST, request.FILES)
        if form.is_valid():
            setup = form.save(commit=False)
            setup.usuario = request.user
            setup.save()
            messages.success(request, "Setup salvo com sucesso!")
            return redirect('meus_setups')
    else:
        # É aqui que a mágica acontece: quando você ENTRA na página,
        # ele cria o formulário vazio para ser exibido.
        form = SetupForm()
    
    return render(request, 'catalogo/meu_setup_novo.html', {'form': form})

def editar_setup_privado(request, setup_id):
    # Busca o setup e garante que pertence ao utilizador logado
    setup = get_object_or_404(Setup, pk=setup_id, usuario=request.user)
    
    if request.method == 'POST':
        # Importante: instance=setup diz que é um UPDATE e não um INSERT
        form = SetupForm(request.POST, request.FILES, instance=setup)
        if form.is_valid():
            setup_editado = form.save(commit=False)
            setup_editado.usuario = request.user # Garante que o dono não muda
            setup_editado.save()
            messages.success(request, "Setup atualizado com sucesso!")
            return redirect('meus_setups')
    else:
        form = SetupForm(instance=setup)
    
    return render(request, 'catalogo/meu_setup_novo.html', {
        'form': form, 
        'editando': True
    })

def deletar_setup_privado(request, setup_id):
    setup = get_object_or_404(Setup, pk=setup_id, usuario=request.user)
    setup.delete()
    messages.success(request, "Setup removido da garagem.")
    return redirect('meus_setups')



def setups_comunidade (request):
    if not request.user.is_authenticated:
        messages.error(request, "Acesso restrito! Faça login para ver os setups.")
        return redirect('login')
    
    setups = SetupPublico.objects.all().order_by('-data_criacao')

    carro_id = request.GET.get('carro')
    pista_id = request.GET.get('pista')
    tipo_id = request.GET.get('tipo')

    if carro_id:
        setups = setups.filter(carro_id=carro_id)
    if pista_id:
        setups = setups.filter(pista_id=pista_id)

    context = {
        'setups_publicos': setups,
        'carros': Carro.objects.all(),
        'pistas': Pista.objects.all(),
        'tipos': SetupPublico.TIPO_CHOICES
    }
    return render(request, 'catalogo/setups_comunidade.html', context)


def setups_comunidade_pesquisa(request):
    carro_id = request.GET.get('carro')
    pista_id = request.GET.get('pista')

    setups = SetupPublico.objects.all()

    if carro_id:
        setups = setups.filter(carro_id=carro_id)
    
    if pista_id:
        setups = setups.filter(pista_id=pista_id)

    context = {
        'setups_publicos': setups,
        'carros': Carro.objects.all(),
        'pistas': Pista.objects.all(),
    }
    return render(request, 'catalogo/setups_comunidade.html', context)

def compartilhar_setup(request, setup_id):
    # Busca o setup privado do piloto
    setup_privado = get_object_or_404(Setup, pk=setup_id, usuario=request.user)

    if request.method == 'POST':
        tipo_escolhido = request.POST.get('tipo')
        
        # Cria o registo na tabela pública (SetupPublico)
        SetupPublico.objects.create(
            usuario=request.user,
            carro=setup_privado.carro,
            pista=setup_privado.pista,
            nome_versao=setup_privado.nome_versao,
            tipo=tipo_escolhido,
            # Copia as referências dos ficheiros .sto
            config_qualy=setup_privado.config_qualy,
            config_qualy_safe=setup_privado.config_qualy_safe,
            config_qualy_rain=setup_privado.config_qualy_rain,
            config_race=setup_privado.config_race,
            config_race_safe=setup_privado.config_race_safe,
            config_race_rain=setup_privado.config_race_rain,
            publicado=False, # Fica invisível até aprovação
            verificado=False
        )
        
        messages.success(request, "Setup enviado! Estará disponível após a moderação.")
        return redirect('meus_setups')

    return render(request, 'catalogo/confirmar_compartilhamento.html', {'setup': setup_privado})
from django.contrib.auth.decorators import user_passes_test

# Função de segurança: apenas o dono do site (superuser) entra aqui
def e_admin(user):
    return user.is_superuser

@user_passes_test(e_admin)
def painel_moderacao(request):
    # Procura apenas setups onde publicado é False
    setups_pendentes = SetupPublico.objects.filter(publicado=False).order_by('-data_criacao')
    return render(request, 'catalogo/moderacao.html', {'setups': setups_pendentes})

@user_passes_test(e_admin)
def aprovar_setup(request, setup_id):
    setup = get_object_or_404(SetupPublico, pk=setup_id)
    setup.publicado = True
    setup.save()
    messages.success(request, f"Setup {setup.nome_versao} aprovado e publicado!")
    return redirect('painel_moderacao')

@user_passes_test(e_admin)
def recusar_setup(request, setup_id):
    setup = get_object_or_404(SetupPublico, pk=setup_id)
    setup.delete() # Remove o setup se for de loja paga
    messages.warning(request, "Setup recusado e removido do sistema.")
    return redirect('painel_moderacao')