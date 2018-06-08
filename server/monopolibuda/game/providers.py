#from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.proxy import Proxy
from random import choice
from operator import attrgetter

class PlayerProvider:
  def get_player(self, game_id, user_id):
    return Proxy().get_player(game_id, user_id)

  def get_active_game_players(self, game_id):
    return Proxy().get_active_game_players(game_id)

  def get_active_game_players_with_order_gt(self, game_id, order):
    return Proxy().get_active_game_players_with_order_gt(game_id, order)

  def get_game_players(self, game_id):
    return Proxy().get_game_players(game_id)

  def get_owner(self, property_id):
    return Proxy().get_owner(property_id)

  def get_player_with_id(self, player_id):
    return Proxy().players_dict[player_id]

  def next_player(self, player_id):
    player = self.get_player_with_id(player_id)
    players = self.get_active_game_players(player.game_id) #Player.objects.filter(game_id=self.game_id, active=True)
    next_players = self.get_active_game_players_with_order_gt(player.game_id, player.order) #players.filter(order__gt=self.order)
    if len(next_players) == 0:
      next_players = players
    return min(next_players,key=attrgetter('order'))

  def skip_turn(self, player_id):
    next_player = self.next_player(player_id)
    self.get_player_with_id(player_id).move = 0
    next_player.move = 2

class PropertyProvider:
  def get_player_properties(self, game_id, player_id):
    return Proxy().get_player_properties(game_id, player_id)
  
  def get_property(self, game_id, player_id, card_id):
    return Proxy().get_property(game_id, player_id, card_id)

  def get_property_with_id(self, property_id):
    return Proxy().propertys_dict[property_id]

  def is_property_taken(self, game_id, card_id):
    return Proxy().is_property_taken(game_id, card_id)

  def check_if_exist(self, game_id, card_id):
    return Proxy().is_property_taken(game_id, card_id)

  def get_property_with_card(self, game_id, card_id):
    return Proxy().get_property_with_card(game_id, card_id)
  
  def get_property_with_position(self, game_id, position):
    return Proxy().get_property_with_position(game_id, position)

class CardProvider:
  def get_card(self, card_id):
    return Proxy().cards_dict[card_id]

  def get_card_with_position(self, position):
    return Proxy().get_card_with_position(position)

class ChargeProvider:
  def get_charge(self, charge_id):
    return Proxy().get_charge(charge_id)

class ChanceProvider:
  def get_chance(self):
    return Proxy().get_chance()

class GameProvider:
  def get_game(self, game_id):
    return Proxy().games_dict[game_id]

  def all(self):
    return list(Proxy().games_dict.values())
