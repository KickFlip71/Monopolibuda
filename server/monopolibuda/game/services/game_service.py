from game.models import Game, Player, User
from game.providers import PlayerProvider
import string
from random import *
from django.core import serializers

class GameService:
  def get_player(self, user_id, game_id):
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

  def get_user(self, user_id):
    user = User.objects.get(pk=user_id)
    return user    

  def skip_turn(self, user_id, game_id):
    player = PlayerProvider().get_player(game_id, user_id)
    if self.__skip_constraint(player):
      player.move = 0
      player.save()
      next_player = player.next_player()
      next_player.move = 2
      next_player.save()
    return player

  def join_player(self, user_id, game_id):
    player = PlayerProvider().get_player(game_id, user_id)
    if(self.__free_slot(game_id) and player == None):
      player_order = Player.objects.filter(game_id=game_id).count() + 1
      player = self.__add_player(user_id, game_id, player_order)
      
    return player

  def remove_player(self, user_id, game_id):
    player = PlayerProvider().get_player(game_id, user_id)
    if(player != None):
      player.delete()

  def set_player_defeated(self, user_id, game_id):
    player = PlayerProvider().get_player(game_id, user_id)    
    if(player != None):
      player.active = False
      player.save()
    return player

  def generate_code(self, code_length):
    allchar = string.ascii_letters
    code = "".join(choice(allchar) for x in range(code_length)).upper()
    return code

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

  def __skip_constraint(self, player):
    return player != None and player.move == 1

  def __free_slot(self, game_id):
    players_amount = Player.objects.filter(game_id=game_id).count()
    allowed_players_amount = Game.objects.filter(id=game_id).first().players_amount
    return players_amount < allowed_players_amount


    