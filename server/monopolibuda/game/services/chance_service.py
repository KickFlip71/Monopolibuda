from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider, ChanceProvider

class ChanceService:
  def __init__(self):
    self.status = 1000

  def get_chance_card(self, game_id, user_id):
    player = PlayerProvider().get_player(game_id,user_id)
    position = player.position
    if position == 3 or position == 9 or position == 15 or position == 21:
      chance_card = ChanceProvider().get_chance()
      if self.__player_exists(player):
        player.update_balance(chance_card.value)
      return chance_card, self.status
    else:
      self.status = 2018
      return None, self.status

  def __player_exists(self, player):
    result = player != None
    if not result:
      self.status = 2002
    return result