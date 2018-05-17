from game.services.game_service import GameService
from game.services.position_service import PositionService
from game.services.card_service import CardService
from game.services.property_service import PropertyService
<<<<<<< HEAD
from game.services.deposit_service import DepositService
=======
from game.services.trading_service import TradingService
>>>>>>> feature/trading
from game.serializers import GameSerializer
from game.serializers import PlayerSerializer
from game.serializers import PropertySerializer
from game.serializers import CardSerializer
from game.models import Player
from game.models import Game
from game.providers import PlayerProvider


class WebsocketService:
  def __init__(self):
    self.response = {
      'status': 1000,
      'payload': None
    }

  def check(self, game_id, user_id):
    record, status = GameService().get_game(game_id=game_id)
    self.__prepare_response(record, status)
    return self.response

  def start(self, game_id):
    game = Game.objects.get(pk=game_id)
    if not game.active:
      PlayerProvider().get_active_game_players(game_id=game_id)[0].enable_move()
      game.set_active()
      self.__prepare_response(game, 1000)
      return self.response
    self.__prepare_response(game, 2000)
    return self.response
    

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

  def end(self, game_id, user_id):
    record, status = GameService().check_bankrupt(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    if status==1000:
      record, status = PropertyService().release_player_properties(game_id=game_id, user_id=user_id)
    return self.response

  def move(self, game_id, user_id):
    record, status = PositionService().move_player(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def offer(self, game_id, user_id):
    record, status = CardService().get_available_card_to_buy(game_id=game_id,user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def tax(self, game_id, user_id):
    record, status = PropertyService().pay_tax(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def buy(self, game_id, user_id):
    record, status = PropertyService().buy_property(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def deposit(self, game_id, user_id, position):
    record, status = DepositService().deposit(game_id=game_id, user_id=user_id, position=position)
    self.__prepare_response(record, status)
    return self.response

  def repurchase(self, game_id, user_id, position):
    record, status = DepositService().repurchase(game_id=game_id, user_id=user_id, position=position)
    self.__prepare_response(record, status)
    return self.response

  def create_offer(self, game_id, user_id, position, price):
    record, status = TradingService().create_offer(game_id=game_id, user_id=user_id, position=position, price=price)
    self.__prepare_response(record, status)
    return self.response

  def accept_offer(self, game_id, user_id, position):
    record, status = TradingService().accept_offer(game_id=game_id, user_id=user_id, position=position)
    self.__prepare_response(record, status)
    return self.response

  def cancel_offer(self, game_id, user_id, position):
    record, status = TradingService().cancel_offer(game_id=game_id, user_id=user_id, position=position)
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
    many = False

    if record.__class__.__name__ == 'list':
      serializer_name = record[0].__class__.__name__
      many = True

    serializer = serializers.get(serializer_name, GameSerializer)
    data = serializer(record, many=many).data

    self.response['status'] = status
    self.response['payload'] = data