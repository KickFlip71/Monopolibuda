from game.models import Game, Player, User
from game.providers import PlayerProvider
import string
from random import *
from django.core import serializers

class GameService:
  def __init__(self):
    self.status = 1000

  def add_game(self, host_id, players_amount):
    code = self.generate_code(code_length=5)
    game = Game(code=code, players_amount=players_amount, host_id=host_id)
    game.save()
    return game, self.status

  def skip_turn(self, user_id, game_id):
    self.status = 1003

    player = PlayerProvider().get_player(game_id, user_id)
    if self.__player_exists(player) and self.__skip_constraint(player):
      player.move = 0
      player.save()
      next_player = player.next_player()
      next_player.move = 2
      next_player.save()
    return player, self.status

  def join_player(self, user_id, game_id):
    self.status = 1001
    player = PlayerProvider().get_player(game_id, user_id)
    if(self.__free_slot(game_id) and not self.__player_exists(player)):
      player_order = Player.objects.filter(game_id=game_id).count() + 1
      player = self.__add_player(user_id, game_id, player_order)
      
    return player, self.status

  def remove_player(self, user_id, game_id):
    self.status = 1002
    player = PlayerProvider().get_player(game_id, user_id)
    if(self.__player_exists(player)):
      player.delete()
    return None, self.status

  def set_player_defeated(self, user_id, game_id):
    player = PlayerProvider().get_player(game_id, user_id)    
    if(self.__player_exists(player)):
      player.defeat()

    return player, self.status

  def get_game(self, game_id):
    game = Game.objects.get(pk=game_id)
    return game, self.status


  def get_user(self, user_id):
    user = User.objects.get(pk=user_id)
    return user 

  def __add_player(self, user_id, game_id, order):
    player = Player(
              user_id=user_id, 
              game_id=game_id,
              balance=3000,
              jailed=0,
              position=0,
              active=True,
              jail_free_card=False,
              move=0,
              order=order,
            )
    player.save()
    return player

  def __player_exists(self, player):
    result = player != None
    if not result:
      self.status = 2002
    return result

  def __skip_constraint(self, player):
    result = player.move == 1
    if not result:
      self.status = 2010
    return result

  def __free_slot(self, game_id):
    players_amount = Player.objects.filter(game_id=game_id).count()
    allowed_players_amount = Game.objects.filter(id=game_id).first().players_amount
    return players_amount < allowed_players_amount

  # TODO: Make it model method instead
  def generate_code(self, code_length):
    allchar = string.ascii_letters
    code = "".join(choice(allchar) for x in range(code_length)).upper()
    return code


    