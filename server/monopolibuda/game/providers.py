from game.models import Property, Game, User, Player, Card, Chance, Charge

class PlayerProvider:
  def get_player(self, game_id, user_id):
    player = Player.objects.filter(game_id=game_id, user_id=user_id).first()
    return player


class PropertyProvider:
  def get_player_properties(self, game_id, player_id):
    properties = Property.objects.filter(game_id=game_id, player_id=player_id)
    return properties

    