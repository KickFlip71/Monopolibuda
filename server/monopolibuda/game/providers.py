from game.models import Property, Game, User, Player, Card, Chance, Charge

class PlayerProvider:
  def get_player(self, game_id, user_id):
    player = Player.objects.filter(game_id=game_id, user_id=user_id).first()
    return player

class PropertyProvider:
  def get_player_properties(self, game_id, player_id):
    properties = Property.objects.filter(game_id=game_id, player_id=player_id)
    return properties
  
  def get_property(self, game_id, player_id, card_id):
    property = Property.objects.get(game_id=game_id, player_id=player_id, card_id=card_id)
    return property

class CardProvider:
  def get_card_with_position(self, position):
    card = Card.objects.get(position=position)
    return card

class ChargeProvider:
  def get_charge(self, charge_id):
    charge = Charge.objects.get(pk=charge_id)
    return charge
