from game.models import User, Game, Player, Property

class PlayerProvider:
  def get_player(self, game_id, user_id):
    player = Player.objects.filter(game_id=game_id, user_id=user_id).first()
    return player