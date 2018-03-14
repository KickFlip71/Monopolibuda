# from django.conf import settings

# from channels.generic.websocket import AsyncJsonWebsocketConsumer

# class GameConsumer(AsyncJsonWebsocketConsumer):

#     async def connect(self):
#         await self.close()

from channels.generic.websocket import SyncConsumer

class GameConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": self.scope["user"].username + " message: " + event["text"],
        })

    def websocket_disconnect(self):
        self.send({
            "type": "websocket.disconnect"        
        })
