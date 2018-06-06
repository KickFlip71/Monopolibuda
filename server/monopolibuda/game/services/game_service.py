from game.models import Game, Player, User
from game.providers import PlayerProvider, GameProvider
from game.proxy import Proxy

from random import *
from django.core import serializers
from django.conf import settings

class GameService:
  def __init__(self):
    self.status = 1000

  def add_game(self, host_id, players_amount):
    game = Game(players_amount=players_amount, host_id=host_id)
    game.save()
    Proxy().games_dict[game.id]=game
    return game, self.status

  def skip_turn(self, user_id, game_id):
    self.status = 1003
    player = PlayerProvider().get_player(game_id, user_id)
    game = GameProvider().get_game(game_id) #Game.objects.get(pk=game_id)

    if (self.__player_exists(player) and self.__skip_constraint(player)) or self.__player_exists(player):
      PlayerProvider().skip_turn(player.id)
    if len(PlayerProvider().get_active_game_players(game_id=game_id))==1:
      self.status=1410

    return game, self.status

  def join_player(self, user_id, game_id):
    self.status = 1001
    player = PlayerProvider().get_player(game_id, user_id)
    if(self.__free_slot(game_id) and player == None):
      player_order = len(PlayerProvider().get_game_players(game_id)) #Player.objects.filter(game_id=game_id).count()
      player = self.__add_player(user_id, game_id, player_order)
      
    return player, self.status

  def remove_player(self, user_id, game_id):
    self.status = 1002
    player = PlayerProvider().get_player(game_id, user_id)
    if(self.__player_exists(player)):
      player.delete()
    return None, self.status

  def check_bankrupt(self, user_id, game_id):
    self.status = 2007
    player = PlayerProvider().get_player(game_id, user_id)
    if(self.__player_exists(player)):
      if(player.is_bankrupt()):
        player.defeat()
        self.status = 1000
    return player, self.status

  # old code:
  def set_player_defeated(self, user_id, game_id):
    self.status = 2002
    player = PlayerProvider().get_player(game_id, user_id)    
    if(self.__player_exists(player)):
      player.defeat()
      self.status = 1000
    return player, self.status
  # end

  def get_game(self, game_id):
    game = GameProvider().get_game(game_id) #Game.objects.get(pk=game_id) 
    return game, self.status

  def __add_player(self, user_id, game_id, order):
    player = Player(
              user_id=user_id, 
              game_id=game_id,
              balance=settings.DEFAULT_GAME_SETTINGS['start_money'],
              jailed=0,
              position=0,
              active=True,
              jail_free_card=False,
              move=0,
              order=order,
            )
    player.save()
    Proxy().players_dict[player.id]=player
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
    players_amount = len(PlayerProvider().get_game_players(game_id)) #Player.objects.filter(game_id=game_id).count()
    allowed_players_amount = GameProvider().get_game(game_id).players_amount #Game.objects.filter(id=game_id).first().players_amount
    return players_amount < allowed_players_amount


    