from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.renderers import JSONRenderer
from game.serializers import GameSerializer
from game.services.game_service import GameService
from random import randint

from game.models import Game #TODO: remove

class GameConsumer(JsonWebsocketConsumer):

  def connect(self):
    self.channel_layer.group_add(
      "all",
      self.channel_name,
    )
    self.accept()
    

  def receive_json(self, content):
    command = content.get("command", None)

    if command == "check":
      self.send_json({
        "command": "check",
        "response": "CONNECTED",
      })
    elif command == "message":
      self.channel_layer.group_send(
      "all",
      {
        "type": "chat.message",
        "user": self.scope["user"].username,
        "message": content['message'],
      })
    elif command == "join":
      self.join_player(self.scope['user'].id)
    elif command == "disconnect":
      self.remove_player(self.scope['user'].id)
    elif command == "move":
      self.channel_layer.group_send(
      "all",
      {
        "type": "board.move",
        "player_id": content["player_id"],
        "response": randint(1,7),
      })
    else:
      self.send_json({
        "response": content.message,
      })

  def chat_message(self, content):
    self.send_json({
      "command": "message",
      "user": content['user'],
      "response": content['message'],
    })

  def join_player(self, user_id):
    game = Game.objects.first() #TODO: Replace with actual game
    GameService().join_player(game_id=game.id, user_id=user_id)
    json = GameSerializer(game).data
    self.send_json({
      "success": "true",
      "response": json,
    })

  def remove_player(self, user_id):
    game = Game.objects.first() #TODO: Replace with actual game
    GameService().remove_player(game_id=game.id, user_id=user_id)
    json = GameSerializer(game).data
    self.send_json({
      "success": "true",
      "response": json,
    })

  def board_move(self, content):
    self.send_json({
      "command": "move",
      "player_id": content['player_id'],
      "response": content['response'],
    })

  def disconnect(self, code):
    self.channel_layer.group_discard(
      "all",
      self.channel_name,
    )
    self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
  })
