from game.models import Property, Game, User, Player, Card, Chance, Charge
from random import choice

class PlayerProvider:
  def get_player(self, game_id, user_id):
    return Player.objects.filter(game_id=game_id, user_id=user_id).first()

  def get_active_game_players(self, game_id):
    return Player.objects.filter(game_id=game_id, active=True)

class PropertyProvider:
  def get_player_properties(self, game_id, player_id):
    return Property.objects.filter(game_id=game_id, player_id=player_id)
  
  def get_property(self, game_id, player_id, card_id):
    return Property.objects.get(game_id=game_id, player_id=player_id, card_id=card_id)

  def is_property_taken(self, game_id, card_id):
    return Property.objects.filter(game_id=game_id, card_id=card_id).exists()

  def check_if_exist(self, game_id, card_id):
    return Property.objects.filter(game_id=game_id,card_id=card_id).exists()

  def get_property_with_card(self, game_id, card_id):
    return Property.objects.filter(game_id=game_id, card_id=card_id).first()
  
  def get_property_with_position(self, game_id, position):
    card = CardProvider().get_card_with_position(position)
    return Property.objects.filter(game_id=game_id, card=card).first()

class CardProvider:
  def get_card_with_position(self, position):
    card = Card.objects.filter(position=position)
    return card[0] if card else None

class ChargeProvider:
  def get_charge(self, charge_id):
    return Charge.objects.get(pk=charge_id)

class ChanceProvider:
  def get_chance(self):
    return choice(Chance.objects.all())
