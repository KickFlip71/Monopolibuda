from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.renderers import JSONRenderer
from asgiref.sync import async_to_sync
from game.serializers import GameSerializer
from game.services.game_service import GameService
from game.services.position_service import PositionService
from random import randint

from game.models import Game #TODO: remove

class GameConsumer(JsonWebsocketConsumer):

  def connect(self):
    if self.scope["user"].is_anonymous:
      self.close()
    
    self.channel_layer.group_add(
      "all",
      self.channel_name
    )
    self.accept()

  def receive_json(self, content):
    command = content.get("command", None)
    content['user_id'] = self.scope['user'].id

    method = getattr(self, command, "check_status")
    method(content)

  def default_message(self, content):
    self.__send_response({
      "response": content.message,
    })

  def message(self, content):
     self.__send_response({
        "user": self.scope["user"].username,
        "message": content['message']
     })

  def check(self, content):
    self.__send_response({
      "command": "check",
      "response": "CONNECTED",
    })

  def join(self, content):
    game = Game.objects.first() #TODO: Replace with actual game
    GameService().join_player(game_id=game.id, user_id=content['user_id'])
    json = GameSerializer(game).data
    self.__send_response(json)


  def leave(self, content):
    game = Game.objects.first() #TODO: Replace with actual game
    GameService().remove_player(game_id=game.id, user_id=content['user_id'])
    json = GameSerializer(game).data
    self.__send_response(json)

  
  def move(self, content):
    game = Game.objects.first() #TODO: Replace with actual game
    player = GameService.get_player(game_id=game.id, user_id=content['user_id'])
    PositionService().change_position(player)
    json = GameSerializer(game).data
    self.__send_response(json)

  def disconnect(self, code):
    self.channel_layer.group_discard(
      "all",
      self.channel_name,
    )
    self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
    })

  def __send_response(self, response, broadcast=True):
    if(broadcast):
      self.channel_layer.group_send("all", {
        "user": response['message'],
      })
      # self.channel_layer.group_send(
      # "all",
      # {
      #   "type": "chat.message",
      #   "response": randint(1,7),
      # })

    else:
      self.send_json(response)
  
  def chat_message(self, event):
    import pdb; pdb.set_trace()
    self.send_json(
      {
        "response": event["response"],
      },
    )