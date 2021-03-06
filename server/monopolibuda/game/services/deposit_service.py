from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider


class DepositService:
  def __init__(self):
      self.status = 1000

  def deposit(self, game_id, user_id, card_id):
      player = PlayerProvider().get_player(game_id,user_id)
      user_property = PropertyProvider().get_property_with_card(game_id=game_id,card_id=card_id)
      self.check_default_validations(player, user_property)
      if self.__is_valid():
        self.is_not_deposited(user_property)
        if self.__is_valid():
          self.__deposit(user_property)
          return PlayerProvider().get_player(game_id,user_id), self.status
      
      return None, self.status

  def repurchase(self, game_id, user_id, card_id):
      player = PlayerProvider().get_player(game_id,user_id)
      user_property = PropertyProvider().get_property_with_card(game_id=game_id,card_id=card_id)
      self.check_default_validations(player, user_property)
      if self.__is_valid():
        self.is_deposited(user_property)
        if self.__is_valid():
          self.__repurchase(user_property)
          return PlayerProvider().get_player(game_id,user_id), self.status
      
      return None, self.status

  def is_not_deposited(self, user_property):
    if user_property.deposited:
      self.status = 2016

  def is_deposited(self, user_property):
    if not user_property.deposited:
      self.status = 2017

  def check_default_validations(self, player, user_property):
    if player == None:
      self.status = 2002
    elif user_property == None:
      self.status = 2007
    elif user_property.player != player:
      self.status = 2004
    elif player.move != 1:
      self.status = 2011

  def __is_valid(self):
    indicator = self.status / 1000
    return indicator == 1

  def __deposit(self, property):
    owner = PlayerProvider().get_owner(property.id)
    card = CardProvider().get_card(property.card_id)
    if not property.deposited:
      property.deposited = True
      owner.balance += card.deposit_value

  def __repurchase(self, property):
    owner = PlayerProvider().get_owner(property.id)
    card = CardProvider().get_card(property.card_id)
    if property.deposited:
      property.deposited = False
      owner.balance -= card.deposit_value