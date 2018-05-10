from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider


class BuildingService:
  def __init__(self):
    self.status = 1000

  def buy_building(self, game_id, user_id):
    player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
    self.__player_exists(player)
    if self.__is_valid():
      user_property = PropertyProvider().get_property_with_position(game_id, player.position)
      self.__property_validations(user_property, player)
      if self.__is_valid():
        self.__player_can_afford(user_property, player)
        self.__max_apartment_reach_limit(user_property)
        if self.__is_valid():
          user_property.buy_building()
          return user_property, self.status
      
    return None, self.status

  def __player_exists(self, player):
    if player == None:
      self.status = 2002

  def __property_validations(self, user_property, player):
    if self.__is_valid() and user_property == None:
      self.status = 2007
    elif self.__is_valid() and user_property.player.id != player.id:
      self.status = 2004

  def __player_can_afford(self, user_property, player):
    building_cost = self.__building_cost(user_property)
    if player.balance < building_cost:
      self.status = 2012

  def __max_apartment_reach_limit(self, user_property):
    if user_property.buildings >= 5:
      self.status = 2014

  def __is_valid(self):
    return (self.status / 1000) == 1

  def __building_cost(self, user_property):
    cost = 0
    if user_property.buildings == 4:
      cost = user_property.card.hotel_cost
    else:
      cost = user_property.card.apartment_cost
    return cost