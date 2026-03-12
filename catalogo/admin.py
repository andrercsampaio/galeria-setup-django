from django.contrib import admin
from .models import Carro, Pista, Setup, SetupPublico

# 1. Configuração para exibir Setups dentro da página do Carro
class SetupInline(admin.TabularInline):
    model = Setup
    extra = 1 # Quantidade de linhas em branco para novos setups

# 2. Configuração da interface de Carros
class CarroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "publicado")
    list_editable = ("publicado",)
    search_fields = ("nome",)
    list_filter = ("categoria",)
    list_per_page = 10
    inlines = [SetupInline]

# 3. Configuração compartilhada para as listagens de Setups (Privados e Públicos)
class ListandoSetups(admin.ModelAdmin):
    list_display = ("id", "carro", "pista", "nome_versao", "usuario")
    list_display_links = ("id", "nome_versao")
    search_fields = ("nome_versao",)
    list_filter = ("carro", "pista", "usuario")
    list_per_page = 10

# 4. Registros Oficiais
admin.site.register(Carro, CarroAdmin)
admin.site.register(Pista)
admin.site.register(Setup, ListandoSetups)
admin.site.register(SetupPublico, ListandoSetups)
