from django.contrib import admin
from .models import Carro, Pista, Setup

# Register your models here.
class SetupInline(admin.TabularInline):
    model = Setup
    extra = 1

class CarroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "publicado")
    list_editable = ("publicado",)
    search_fields = ("nome",)
    list_filter = ("categoria",)
    list_editable = ("publicado",)
    list_per_page = 10
    inlines = [SetupInline]

admin.site.register(Carro, CarroAdmin)
admin.site.register(Pista)
admin.site.register(Setup)
