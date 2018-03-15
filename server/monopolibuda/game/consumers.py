from channels.generic.websocket import AsyncJsonWebsocketConsumer
from random import randint

class GameConsumer(AsyncJsonWebsocketConsumer):

  async def connect(self):
    await self.channel_layer.group_add(
      "all",
      self.channel_name,
    )
    await self.accept()

  async def receive_json(self, content):
    command = content.get("command", None)

    if command == "check":
      await self.send_json({
        "command": "check",
        "response": "CONNECTED",
      })
    elif command == "message":
      await self.channel_layer.group_send(
      "all",
      {
        "type": "chat.message",
        "user": self.scope["user"].username,
        "message": content['message'],
      })
    elif command == "move":
      await self.channel_layer.group_send(
      "all",
      {
        "type": "board.move",
        "player_id": content["player_id"],
        "response": randint(1,7),
      })
    else:
      await self.send_json({
        "response": content.message,
      })

  async def chat_message(self, content):
    await self.send_json({
      "command": "message",
      "user": content['user'],
      "response": content['message'],
    })

  async def board_move(self, content):
    await self.send_json({
      "command": "move",
      "player_id": content['player_id'],
      "response": content['response'],
    })

  async def disconnect(self, code):
    await self.channel_layer.group_discard(
      "all",
      self.channel_name,
    )
    await self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
  })
