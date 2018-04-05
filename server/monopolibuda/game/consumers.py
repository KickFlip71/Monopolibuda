from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework.renderers import JSONRenderer
from game.serializers import GameSerializer, PlayerSerializer, PropertySerializer
from game.services.game_service import GameService
from game.services.position_service import PositionService
from random import randint

from game.models import Game #TODO: remove

class GameConsumer(JsonWebsocketConsumer):

  def connect(self):
    if self.scope["user"].is_anonymous:
      self.close()
    
    async_to_sync(self.channel_layer.group_add)(
      'all',
      self.channel_name
    )
    self.accept()

  def receive_json(self, content):
    command = content.get("command", None)
    content['user'] = self.scope['user']
    content['game'] = Game.objects.first() # TODO: temporary hardcoded
    method = getattr(self, command, self.wrong_command)
    method(content)

  def message(self, content):
     self.send_response({
        "user": self.scope["user"].username,
        "message": content['message']
     })

  def wrong_command(self, content):
     self.send_response({
        "error": "Command not supported"
     })

  def check(self, content):
    self.send_response(
      {
        "command": "check",
        "response": "connected"
      },
      False
    )

  def join(self, content):
    player = GameService().join_player(game_id=content['game'].id, user_id=content['user'].id)
    self.__respond_with(player, "player", "playerdata", broadcast=False)
    self.__respond_with(player, "player", "board_join")

  def skip(self, content):
    player = GameService().skip_turn(game_id=content['game'].id, user_id=content['user'].id)
    self.__respond_with(player, "player", "skip")

  def leave(self, content):
    GameService().remove_player(game_id=content['game'].id, user_id=content['user'].id)
    self.__respond_with(content['game'], "game", "leave")    
  
  def move(self, content):
    player = PositionService().move_player(game_id=content['game'].id, user_id=content['user'].id)
    self.__respond_with(player, "player", "board_move")

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      "all",
      self.channel_name,
    )
    self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
    })

  def __respond_with(self, record, response_type, command, broadcast=True):
    serializers = {
      "game": GameSerializer,
      "player": PlayerSerializer,
      "property": PropertySerializer
    }

    serializer = serializers.get(response_type, GameSerializer)
    data = serializer(record).data
    response = self.__prepare_response(data, command)
    self.send_response(response, broadcast)

  def __prepare_response(self, data, command, errors = {}):
    response = {}
    success = not bool(errors)

    response['payload'] = data
    response['command'] = command
    response['errors'] = errors
    response['success'] = success
    return response

  def send_response(self, response, broadcast=True):
    if(broadcast):
      async_to_sync(self.channel_layer.group_send)(
      "all",
      {
        "type": "broadcast",
        "response": response
      })
    else:
      self.send_json(response)
  
  # usable only with send_response with arg broadcast=True
  def broadcast(self, content):
    self.send_json(content["response"])

