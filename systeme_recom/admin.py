from django.contrib import admin

from django.contrib import admin
from .models import Culture ,Temperature,Pluviometrie,Region
# Register your models here.
admin.site.register(Region)
admin.site.register(Culture)
admin.site.register(Pluviometrie)
admin.site.register(Temperature)

