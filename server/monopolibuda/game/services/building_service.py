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
        self.__is_deposited(user_property)        
        #self.__player_can_afford(user_property, player) <- git gud
        self.__player_has_move(player)
        self.__max_apartment_reach_limit(user_property)
        if self.__is_valid():
          self.__buy_building(user_property)
          return PlayerProvider().get_player(game_id=game_id, user_id=user_id), self.status
      
    return None, self.status

  def sell_building(self, game_id, user_id, card_id):
    player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
    self.__player_exists(player)
    if self.__is_valid():
      user_property = PropertyProvider().get_property_with_card(game_id, card_id=card_id)
      self.__property_validations(user_property, player)
      if self.__is_valid():
        self.__is_deposited(user_property)
        self.__player_has_move(player)
        self.__min_apartment_reach_limit(user_property)
        if self.__is_valid():
          self.__sell_building(user_property)
          return PlayerProvider().get_player(game_id=game_id, user_id=user_id), self.status
      
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

  def __min_apartment_reach_limit(self, user_property):
    if user_property.buildings == 0:
      self.status = 2015

  def __is_deposited(self, user_property):
    if user_property.deposited:
      self.status = 2016

  def __is_valid(self):
    return (self.status / 1000) == 1

  def __building_cost(self, user_property):
    cost = 0
    card = CardProvider().get_card(user_property.card_id)
    if user_property.buildings == 4:
      cost = card.hotel_cost
    else:
      cost = card.apartment_cost
    return cost

  def __player_has_move(self, player):
    if(player.move != 1):
      self.status = 2011

  def __buy_building(self, property):
    owner = PlayerProvider().get_owner(property.id)
    property.buildings += 1
    card = CardProvider().get_card(property.card_id)
    if property.buildings == 5:
      owner.balance -= card.hotel_cost
    elif property.buildings < 5 and property.buildings > 0:
      owner.balance -= card.apartment_cost

  def __sell_building(self, property):
    owner = PlayerProvider().get_owner(property.id)
    card = CardProvider().get_card(property.card_id)
    if property.buildings == 5:
      property.buildings -= 1
      owner.balance += card.hotel_cost
    elif property.buildings >= 0:
      property.buildings -= 1            
      owner.balance += card.apartment_cost
