from game.models import Game, Player
import string
from random import *
from django.core import serializers
import pdb

class GameService:
  def get_player(self, game_id, user_id):
    player = Player.objects.filter(game_id=game_id, user_id=user_id).first()
    return player

  def add_game(self, host_id, players_amount):
    code = self.generate_code(code_length=5)
    game = Game(code=code, players_amount=players_amount, host_id=host_id)
    game.save()
    return game

  def get_game(self, game_id):
    game = Game.objects.get(pk=game_id)
    return game

  def add_player(self, user_id, game_id):
    player = Player(
              user_id=user_id, 
              game_id=game_id,
              balance=3000,
              jailed=0,
              position=0,
              active=True,
              jail_free_card=False,
              move=0,
            )
    player.save()
    return player

  def remove_player(self, user_id, game_id):
    player = self.get_player(user_id, game_id)
    player.delete()

  def set_player_defeated(self, player_id):
    player = Player.objects.get(pk=player_id)
    player.active = False
    player.save()
    return player

  def generate_code(self, code_length):
    allchar = string.ascii_letters
    code = "".join(choice(allchar) for x in range(code_length)).upper()
    return code


    