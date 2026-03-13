from django import forms
from catalogo.models import Setup

class SetupForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = [
            'carro', 'pista', 'nome_versao', 
            'config_qualy', 'config_qualy_safe', 'config_qualy_rain',
            'config_race', 'config_race_safe', 'config_race_rain'
        ]
        
    def clean(self):
        """
        Função que valida o formulário inteiro de uma vez.
        """
        # Primeiro, pegamos todos os dados que o piloto preencheu
        cleaned_data = super().clean()

        # Criamos uma lista com os nomes de todos os campos de arquivo
        campos_de_arquivo = [
            'config_qualy', 'config_qualy_safe', 'config_qualy_rain',
            'config_race', 'config_race_safe', 'config_race_rain'
        ]

        # Agora, passamos por cada campo da lista para verificar a extensão
        for campo in campos_de_arquivo:
            arquivo = cleaned_data.get(campo)

            # Se o piloto subiu algum arquivo nesse campo específico...
            if arquivo:
                # Verificamos se o nome do arquivo NÃO termina com .sto
                if not arquivo.name.lower().endswith('.sto'):
                    # Se não for .sto, o Django adiciona um erro direto no campo certo
                    self.add_error(campo, "Formato inválido! Envie apenas arquivos .sto")

        # Retornamos os dados limpos e validados
        return cleaned_data