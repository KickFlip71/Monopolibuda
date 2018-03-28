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
    content['user_id'] = self.scope['user'].id

    method = getattr(self, command, "check_status")
    method(content)

  def default_message(self, content):
    self.send_response({
      "response": content.message,
    })

  def message(self, content):
     self.send_response({
        "user": self.scope["user"].username,
        "message": content['message']
     })

  def check(self, content):
    self.send_response(
      {
        "command": "check",
        "response": "connected"
      }
    )


  def join(self, content):
    game = Game.objects.first() #TODO: Replace with actual game
    user = content['user_id']
    GameService().join_player(game_id=game.id, user_id=user)
    self.__respond_with(game, "game")

  def leave(self, content):
    game = Game.objects.first() #TODO: Replace with actual game
    user = content['user_id']
    GameService().remove_player(game_id=game.id, user_id=user)
    self.__respond_with(game, "game")    

  
  def move(self, content):
    game = Game.objects.first() #TODO: Replace with actual game
    user = content['user_id']
    player = GameService().get_player(game_id=game.id, user_id=user)
    PositionService().change_position(player)
    self.__respond_with(game, "game")

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      "all",
      self.channel_name,
    )
    self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
    })

  def __respond_with(self, record, response_type, broadcast=True):
    serializers = {
      "game": GameSerializer,
      "player": PlayerSerializer,
      "property": PropertySerializer
    }

    serializer = serializers.get(response_type, GameSerializer)
    json = serializer(record).data
    self.send_response(json, broadcast)

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

