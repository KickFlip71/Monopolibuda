from django.contrib import admin

# Register your models here.
from .models import Game, Player, Property, Card, Chance, Charge

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Property)
admin.site.register(Card)
admin.site.register(Chance)
admin.site.register(Charge)