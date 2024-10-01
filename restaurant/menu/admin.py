from django.contrib import admin
from .models import Menu, TableReservation, Orders, Profile, Sale

admin.site.register(Menu)
admin.site.register(TableReservation)
admin.site.register(Orders)
admin.site.register(Profile)
admin.site.register(Sale)