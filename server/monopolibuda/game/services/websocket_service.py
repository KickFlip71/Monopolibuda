from game.services.game_service import GameService
from game.services.position_service import PositionService
from game.services.card_service import CardService
from game.serializers import GameSerializer
from game.serializers import PlayerSerializer
from game.serializers import PropertySerializer
from game.serializers import CardSerializer
from game.models import Player
from game.providers import PlayerProvider


class WebsocketService:
  def __init__(self):
    self.response = {
      'status': 1000,
      'payload': None
    }

  def join(self, game_id, user_id):
    record, status = GameService().join_player(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def leave(self, game_id, user_id):
    record, status = GameService().remove_player(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response
  
  def skip(self, game_id, user_id):
    record, status = GameService().skip_turn(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response
  
  def move(self, game_id, user_id):
    record, status = PositionService().move_player(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def offer(self, game_id, user_id):
    record, status = CardService().get_available_card_to_buy(game_id=game_id,user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def __prepare_response(self, record, status = 1000):
    serializers = {
      "Game": GameSerializer,
      "Player": PlayerSerializer,
      "Property": PropertySerializer,
      "Card": CardSerializer
    }
    serializer_name = record.__class__.__name__


    serializer = serializers.get(serializer_name, GameSerializer)
    data = serializer(record).data

    self.response['status'] = status
    self.response['payload'] = data