from game.services.game_service import GameService
from game.services.position_service import PositionService
from game.serializers import GameSerializer
from game.serializers import PlayerSerializer
from game.serializers import PropertySerializer
from game.models import Player
from game.providers import PlayerProvider


class WebsocketService:
  def __init__(self):
    self.response = {
      'error': 1000,
      'payload': None
    }

  def join(self, game_id, user_id):
    record = GameService().join_player(game_id=game_id, user_id=user_id)
    error = 1201
    self.__prepare_response(record, error)
    return self.response

  def leave(self, game_id, user_id):
    record = GameService().remove_player(game_id=game_id, user_id=user_id)
    error = 1202
    self.__prepare_response(record, error)
    return self.response
  
  def skip(self, game_id, user_id):
    record = GameService().skip_turn(game_id=game_id, user_id=user_id)
    error = 1203
    self.__prepare_response(record, error)
    return self.response
  
  def move(self, game_id, user_id):
    record = PositionService().move_player(game_id=game_id, user_id=user_id)
    error = 1204
    self.__prepare_response(record, error)
    return self.response

  def __prepare_response(self, record, error = 1000):
    serializers = {
      "Game": GameSerializer,
      "Player": PlayerSerializer,
      "Property": PropertySerializer
    }
    serializer_name = record.__class__.__name__


    serializer = serializers.get(serializer_name, GameSerializer)
    data = serializer(record).data

    self.response['error'] = error
    self.response['payload'] = data