from game.services.game_service import GameService
from game.services.position_service import PositionService
from game.services.card_service import CardService
from game.services.property_service import PropertyService
from game.services.deposit_service import DepositService
from game.services.trading_service import TradingService
from game.services.building_service import BuildingService
from game.services.chance_service import ChanceService
from game.serializers import GameSerializer
from game.serializers import PlayerSerializer
from game.serializers import PropertySerializer
from game.serializers import CardSerializer
from game.serializers import ChanceSerializer
from game.models import Player
from game.models import Game
from game.proxy import Proxy
from game.providers import PlayerProvider, GameProvider


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
    game = GameProvider().get_game(game_id)
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
  
  def skip(self, game_id, user_id):
    TradingService().cancel_players_offers(game_id=game_id, user_id=user_id)
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

  def deposit(self, game_id, user_id, card_id):
    record, status = DepositService().deposit(game_id=game_id, user_id=user_id, card_id=card_id)
    self.__prepare_response(record, status)
    return self.response

  def repurchase(self, game_id, user_id, card_id):
    record, status = DepositService().repurchase(game_id=game_id, user_id=user_id, card_id=card_id)
    self.__prepare_response(record, status)
    return self.response

  def create_offer(self, game_id, user_id, card_id, price):
    record, status = TradingService().create_offer(game_id=game_id, user_id=user_id, card_id=card_id, price=price)
    self.__prepare_response(record, status)
    return self.response

  def accept_offer(self, game_id, user_id, card_id):
    record, status = TradingService().accept_offer(game_id=game_id, user_id=user_id, card_id=card_id)
    self.__prepare_response(record, status)
    return self.response

  def cancel_offer(self, game_id, user_id, card_id):
    record, status = TradingService().cancel_offer(game_id=game_id, user_id=user_id, card_id=card_id)
    self.__prepare_response(record, status)
    return self.response

  def buy_building(self, game_id, user_id):
    record, status = BuildingService().buy_building(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def sell_building(self, game_id, user_id, card_id):
    record, status = BuildingService().sell_building(game_id=game_id, user_id=user_id, card_id=card_id)
    self.__prepare_response(record, status)
    return self.response

  def chance(self, game_id, user_id):
    record, status = ChanceService().get_chance_card(game_id=game_id, user_id=user_id)
    self.__prepare_response(record, status)
    return self.response

  def __prepare_response(self, record, status = 1000):
    serializers = {
      "Game": Proxy().get_serialized_game,
      "Player": Proxy().get_serialized_player,
      "Property": Proxy().get_serialized_property,
      "Card": Proxy().get_serialized_card,
      "Chance": Proxy().get_serialized_chance
    }
    serializer_name = record.__class__.__name__
    many = False

    if record.__class__.__name__ == 'list':
      serializer_name = record[0].__class__.__name__
      many = True

    serializer = serializers.get(serializer_name, Proxy().get_serialized_game)
    data = serializer(record, many=many)

    self.response['status'] = status
    self.response['payload'] = data