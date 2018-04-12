from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework.renderers import JSONRenderer
from game.serializers import GameSerializer, PlayerSerializer, PropertySerializer
from game.services.game_service import GameService
from game.services.websocket_service import WebsocketService
from game.services.position_service import PositionService
from random import randint

from game.models import Game #TODO: remove

class GameConsumer(JsonWebsocketConsumer):

  def connect(self):
    if self.scope["user"].is_anonymous:
      self.close()

    code = self.scope["url_route"]["kwargs"]["code"]
    game_id = self.scope["url_route"]["kwargs"]["game_id"]

    if not self.__auth_player(game_id=game_id, code=code):
      self.close()
    
    async_to_sync(self.channel_layer.group_add)(
      str(game_id),
      self.channel_name
    )
    self.accept()

  def receive_json(self, content):
    game_id = self.scope["url_route"]["kwargs"]["game_id"]
    
    command = content.get("command", None)
    content['user'] = self.scope['user']
    content['game'] = Game.objects.get(pk=game_id) # TODO: temporary hardcoded
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
    response = WebsocketService().check(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'check'
    self.send_response(response, broadcast=False)

  def join(self, content):
    response = WebsocketService().join(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'board_join'    
    self.send_response(response)
    response['command'] = 'player_join'
    self.send_response(response, broadcast=False)


  def skip(self, content):
    response = WebsocketService().skip(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'board_skip'
    self.send_response(response)
    response['command'] = 'player_skip'
    self.send_response(response)

  def leave(self, content):
    response = WebsocketService().leave(game_id=content['game'].id, user_id=content['user'].id)    
    response['command'] = 'player_leave'
    self.send_response(response)   
  
  def move(self, content):
    response = WebsocketService().move(game_id=content['game'].id, user_id=content['user'].id)        
    response['command'] = 'board_move'
    print(response['command'])
    self.send_response(response)
    response['command'] = 'player_move'
    self.send_response(response, broadcast=False)

  def buy(self, content):
    #TODO
    pass

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      "all",
      self.channel_name,
    )
    self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
    })


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

  def __auth_player(self, game_id, code):
    auth = False
    if Game.objects.get(pk=game_id).host_id == self.scope['user'].id:
      auth = True
    if Game.objects.get(pk=game_id).code == code:
      auth = True
    return auth