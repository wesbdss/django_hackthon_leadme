from django.contrib import admin
from .models import  Leads
# Register your models here.


class LeadsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo')



admin.site.register(Leads, LeadsAdmin)