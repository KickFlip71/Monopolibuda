from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    code = models.CharField(max_length=50)
    players_amount = models.IntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)

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
        

class Charge(models.Model):
    zero_apartments = models.IntegerField()
    one_apartments = models.IntegerField()
    two_apartments = models.IntegerField()
    three_apartments = models.IntegerField()
    four_apartments = models.IntegerField()
    five_apartments = models.IntegerField()

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
    buildings = models.IntegerField()
    deposited = models.BooleanField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

class Chance(models.Model):
    chance_type = models.IntegerField()
    description = models.CharField(max_length=500)
    value = models.IntegerField()
