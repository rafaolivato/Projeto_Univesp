from django.contrib import admin
from .models import Paciente, Produto

admin.site.register(Paciente)
admin.site.register(Produto)