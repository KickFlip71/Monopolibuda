from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import string
from random import *

class Game(models.Model):
    code = models.CharField(max_length=50)
    players_amount = models.IntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        allchar = string.ascii_letters
        self.code = "".join(choice(allchar) for x in range(settings.DEFAULT_GAME_SETTINGS['code_len'])).upper()
        super(Game, self).save(*args, **kwargs)

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    balance = models.IntegerField()
    jailed = models.IntegerField()
    position = models.IntegerField()
    active = models.BooleanField()
    jail_free_card = models.BooleanField()
    move = models.IntegerField()
    order = models.IntegerField()

    def next_player(self):
        players_count = Player.objects.filter(game_id=self.game_id).count()
        next_player_order = (self.order + 1) % players_count
        return Player.objects.filter(game_id=self.game_id, order=next_player_order).first()

    def skip_turn(self):
        next_player = self.next_player()
        self.move = 0
        next_player.move = 2
        self.save()
        next_player.save()

    def defeat(self):
        self.active = False
        self.save()

    def update_balance(self, money):
        self.balance += money
        self.save()

    def reset_balance(self):
        self.balance = 0
        self.save()

    def can_pay_tax(self, tax):
        return self.balance >= tax

    def is_bankrupt(self):
        return self.balance < 0

    def disable_move(self):
        self.move = 1
        self.save()

    def check_position(self):
        return self.position >= settings.DEFAULT_GAME_SETTINGS['field_count']

    def fix_position(self):
        self.position = self.position % settings.DEFAULT_GAME_SETTINGS['field_count']
        self.save()

class Charge(models.Model):
    zero_apartments = models.IntegerField()
    one_apartments = models.IntegerField()
    two_apartments = models.IntegerField()
    three_apartments = models.IntegerField()
    four_apartments = models.IntegerField()
    five_apartments = models.IntegerField()

    def get_charge_for_amount_of_buildings(self, buildings):
        if buildings == 0:
            return self.zero_apartments
        elif buildings == 1:
            return self.one_apartments
        elif buildings == 2:
            return self.two_apartments
        elif buildings == 3:
            return self.three_apartments
        elif buildings == 4:
            return self.four_apartments
        else:
            return self.five_apartments

class Card(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    apartment_cost = models.IntegerField()
    hotel_cost = models.IntegerField()
    deposit_value = models.IntegerField()
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    group_number = models.IntegerField()
    position = models.IntegerField()

class Property(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    buildings = models.IntegerField(default=0)
    deposited = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

class Chance(models.Model):
    chance_type = models.IntegerField()
    description = models.CharField(max_length=500)
    value = models.IntegerField()
