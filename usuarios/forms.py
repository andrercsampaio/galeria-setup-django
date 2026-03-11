from django import forms

class LoginForms(forms.Form):
    nome_login = forms.CharField(
        label="Nome de Login", 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "sidebar-btn", # Usando sua classe de botão/input
                "style": "background-color: #29292e; color: white; width: 100%; margin-bottom: 15px;",
                "placeholder": "Ex: AndreSilva"
            }
        )
    )
    senha = forms.CharField(
        label="Senha", 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "sidebar-btn",
                "style": "background-color: #29292e; color: white; width: 100%;",
                "placeholder": "Digite sua senha"
            }
        )
    )

class CadastroForms(forms.Form):
    nome_completo = forms.CharField(
        label="Nome Completo", 
        required=True, 
        max_length=100,
        widget=forms.TextInput(attrs={"class": "sidebar-btn", "placeholder": "Ex: André Silva"})
    )
    nome_usuario = forms.CharField(
        label="Nome de Usuário (Nickname)", 
        required=True, 
        max_length=30,
        widget=forms.TextInput(attrs={"class": "sidebar-btn", "placeholder": "Ex: Andre99"})
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={"class": "sidebar-btn", "placeholder": "Ex: andre@email.com"})
    )
    senha_1 = forms.CharField(
        label="Senha", 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(attrs={"class": "sidebar-btn", "placeholder": "Digite sua senha"})
    )
    senha_2 = forms.CharField(
        label="Confirme sua senha", 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(attrs={"class": "sidebar-btn", "placeholder": "Digite novamente"})
    )

    # VALIDAÇÃO: Impede espaços no nome de usuário
    def clean_nome_usuario(self):
        nome = self.cleaned_data.get('nome_usuario')
        if nome:
            nome = nome.strip()
            if " " in nome:
                raise forms.ValidationError("Espaços não são permitidos no nome de usuário")
            return nome

    # VALIDAÇÃO: Compara as senhas
    # Dentro da classe CadastroForms
    def clean(self):
        cleaned_data = super().clean()
        senha_1 = cleaned_data.get('senha_1')
        senha_2 = cleaned_data.get('senha_2')

        if senha_1 and senha_2:
            if senha_1 != senha_2:
                self.add_error('senha_2', 'As senhas não são iguais')
        
        return cleaned_data # <--- ESTE RETURN É OBRIGATÓRIO