from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider


class TradingService:
    def __init__(self):
        self.status = 1000

    def create_offer(self, game_id, user_id, card_id, price):
      player = PlayerProvider().get_player(game_id, user_id)
      user_property = PropertyProvider().get_property_with_card(game_id, card_id)
      self.__default_validations(player, user_property)
      self.__property_owner_validations(player, user_property)
      self.__player_has_move(player)

      if self.__is_valid():
        user_property.for_sell(price)
        return user_property, self.status
      else:
        return None, self.status        

    def accept_offer(self, game_id, user_id, card_id):
      new_owner = PlayerProvider().get_player(game_id, user_id)
      user_property = PropertyProvider().get_property_with_card(game_id, card_id)
      old_owner = PlayerProvider().get_owner(property_id=user_property.id)
      self.__default_validations(new_owner, user_property)
      self.__property_for_sale(user_property)
      self.__player_can_afford(new_owner, user_property)

      if self.__is_valid():
        self.__finish_exchange(new_owner, old_owner, user_property)
        return [new_owner, old_owner], self.status
      else:
        return None, self.status  

    def cancel_offer(self, game_id, user_id, card_id):
      player = PlayerProvider().get_player(game_id, user_id)
      user_property = PropertyProvider().get_property_with_card(game_id, card_id)
      self.__default_validations(player, user_property)
      self.__property_owner_validations(player, user_property)
      self.__property_for_sale(user_property)

      if self.__is_valid():
        user_property.cancel_offer()
        return user_property, self.status
      else:
        return None, self.status

    def cancel_players_offers(self, game_id, user_id):
      player = PlayerProvider().get_player(game_id, user_id)
      user_properties = PropertyProvider().get_player_properties(game_id=game_id,player_id=player.id)
      for user_property in user_properties:
        self.__property_for_sale(user_property)
        if self.__is_valid():
          user_property.cancel_offer()

    def __finish_exchange(self, new_owner, old_owner, user_property):
      user_property.change_owner(new_owner, old_owner)

    def __property_for_sale(self, user_property):
      if user_property.selling_price == 0:
        self.status = 2013

    def __property_owner_validations(self, player, user_property):
      if user_property.player_id != player.id:
        self.status = 2004

    def __player_can_afford(self, player, user_property):
      if player.balance < user_property.selling_price:
        self.status = 2012

    def __player_has_move(self, player):
      if player.move != 1:
        self.status = 2010

    def __default_validations(self, player, user_property):
      if player == None:
        self.status = 2002
      elif user_property == None:
        self.status = 2007

    def __is_valid(self):
      return (self.status / 1000) == 1