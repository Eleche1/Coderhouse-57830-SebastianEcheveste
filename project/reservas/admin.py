from django.contrib import admin
from .models import Cliente, Cancha, Reserva, UserProfile

admin.site.register(Cliente)
admin.site.register(Cancha)
admin.site.register(Reserva)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture']
