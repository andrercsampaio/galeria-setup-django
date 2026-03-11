from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib import auth, messages
from django.contrib.auth.models import User

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()

            usuario = auth.authenticate(
                request, 
                username=nome,
                password=senha
            )
        
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f'{nome}, logado com sucesso')
                return redirect('index')
            else:
                messages.error(request, 'Erro ao efetuar login')
                return redirect('login')

    return render(request, 'usuarios/login.html', {"form": form})

def logout(request):
    auth.logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
    return redirect('login')

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            print("Formulário Válido!")
            # USAR cleaned_data em vez de .value() é a forma correta no Django
            nome_completo = form.cleaned_data.get('nome_completo')
            nome_usuario = form.cleaned_data.get('nome_usuario')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha_1')

            # Verifica se o Nickname já existe no Banco de Dados
            if User.objects.filter(username=nome_usuario).exists():
                messages.error(request, 'Este nome de utilizador já está em uso')
                return redirect('cadastro')

            # Criação do utilizador com senha criptografada (Hash)
            usuario = User.objects.create_user(
                username=nome_usuario,
                email=email,
                password=senha,
                first_name=nome_completo
            )
            usuario.save()
            messages.success(request, 'Piloto cadastrado com sucesso!')
            return redirect('login')
        else:
            # DEBUG: Se o formulário for inválido, isto aparecerá no seu terminal (VS Code)
            print(form.errors) 
            messages.error(request, 'Erro no cadastro. Verifique os campos abaixo.')

    return render(request, 'usuarios/cadastro.html', {"form": form})