from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider


class TradingService:
    def __init__(self):
        self.status = 1000

    def offer_inquiry(self, game_id, user_id, position, price):
      player = PlayerProvider().get_player(game_id, user_id)
      user_property = PropertyProvider().get_property_with_position(game_id, position)
      self.__default_validations(player, user_property)
      self.__property_owner_validations(player, user_property)

      if self.__is_valid():
        user_property.for_sell(price)
        return user_property, self.status
      else:
        return None, self.status        

    def accept_offer(self, game_id, user_id, position):
      player = PlayerProvider().get_player(game_id, user_id)
      user_property = PropertyProvider().get_property_with_position(game_id, position)
      self.__default_validations(player, user_property)
      self.__property_for_sale(user_property)
      self.__player_can_afford(player, user_property)

      if self.__is_valid():
        self.__finish_exchange(player, user_property)
        return player, self.status
      else:
        return None, self.status  

    def cancel_offer(self, game_id, user_id, position):
      player = PlayerProvider().get_player(game_id, user_id)
      user_property = PropertyProvider().get_property_with_position(game_id, position)
      self.__default_validations(player, user_property)
      self.__property_owner_validations(player, user_property)
      self.__property_for_sale(user_property)

      if self.__is_valid():
        user_property.cancel_offer()
        return user_property, self.status
      else:
        return None, self.status  

    def __finish_exchange(self, player, user_property):
      user_property.change_owner(player)

    def __property_for_sale(self, user_property):
      if self.__is_valid() and user_property.selling_price == 0:
        self.status = 2013

    def __property_owner_validations(self, player, user_property):
      if self.__is_valid() and user_property.player_id != player.id:
        self.status = 2004

    def __player_can_afford(self, player, user_property):
      if self.__is_valid() and player.balance < user_property.selling_price:
        self.status = 2012

    def __default_validations(self, player, user_property):
      if player == None:
        self.status = 2002
      elif user_property == None:
        self.status = 2007

    def __is_valid(self):
      return (self.status / 1000) == 1