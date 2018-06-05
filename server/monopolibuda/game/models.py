from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import string
from random import *

class Game(models.Model):
    code = models.CharField(max_length=50)
    players_amount = models.IntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        allchar = string.ascii_letters
        if(len(self.code)==0):
            self.code = "".join(choice(allchar) for x in range(settings.DEFAULT_GAME_SETTINGS['code_len'])).upper()
        super(Game, self).save(*args, **kwargs)

    def set_active(self):
        self.active = True

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

    def defeat(self):
        self.active = False

    def update_balance(self, money):
        self.balance += money

    def reset_balance(self):
        self.balance = 0

    def can_pay_tax(self, tax):
        return self.balance >= tax

    def is_bankrupt(self):
        return self.balance < 0

    def enable_move(self):
        self.move = 2

    def disable_move(self):
        self.move = 1

    def check_position(self):
        return self.position >= settings.DEFAULT_GAME_SETTINGS['field_count']

    def fix_position(self):
        self.position = self.position % settings.DEFAULT_GAME_SETTINGS['field_count']

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
    selling_price = models.IntegerField(default=0)

    def change_owner(self, new_owner, old_owner):
        self.player = new_owner
        price = self.selling_price
        new_owner.balance -= price
        old_owner.balance += price
        self.selling_price = 0

    def for_sell(self, price):
        self.selling_price = price

    def cancel_offer(self):
        self.selling_price = 0

    def deposit(self):
        owner = self.player
        if not self.deposited:
            self.deposited = True
            owner.balance += self.card.deposit_value

    def repurchase(self):
        owner = self.player
        if self.deposited:
            self.deposited = False
            owner.balance -= self.card.deposit_value

    def buy_building(self):
        owner = self.player
        self.buildings += 1
        if self.buildings == 5:
            owner.balance -= self.card.hotel_cost
        elif self.buildings < 5 and self.buildings > 0:
            owner.balance -= self.card.apartment_cost

    def sell_building(self):
        owner = self.player
        if self.buildings == 5:
            self.buildings -= 1
            owner.balance += self.card.hotel_cost
        elif self.buildings >= 0:
            self.buildings -= 1            
            owner.balance += self.card.apartment_cost

class Chance(models.Model):
    chance_type = models.IntegerField()
    description = models.CharField(max_length=500)
    value = models.IntegerField()
