from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework.renderers import JSONRenderer
from game.services.game_service import GameService
from game.services.websocket_service import WebsocketService
from game.proxy import Proxy
from random import randint
from game.proxy import Proxy
from game.models import Game
import threading
import time

class SyncWithDatebaseThread(object):
  def __init__(self, interval):
    self.interval = interval
    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):
    while True:
      Proxy().save()
      time.sleep(self.interval)


class GameConsumer(JsonWebsocketConsumer):
  Proxy()
  SyncWithDatebaseThread(120)
  
  def connect(self):
    if self.scope["user"].is_anonymous:
      self.close()

    code = self.__get_code()
    game_id = self.__get_game()

    if not self.__auth_player(game_id=game_id, code=code):
      self.close()
    
    async_to_sync(self.channel_layer.group_add)(
      self.__get_game(),
      self.channel_name
    )
    self.accept()

  def receive_json(self, content):
    game_id = self.__get_game()
    command = content.get("command", None)
    content['user'] = self.scope['user']
    content['game'] = Game.objects.get(pk=game_id)
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

  def start(self, content):
    response = WebsocketService().start(game_id=content['game'].id)
    if response['status'] == 1000:
      response['command'] = 'start'
      self.send_response(response)
    

  def join(self, content):
    response = WebsocketService().join(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'board_join'    
    self.send_response(response)
    response['command'] = 'player_join'
    self.send_response(response, broadcast=False)

  def skip(self, content):
    response_tax = WebsocketService().tax(game_id=content['game'].id, user_id=content['user'].id)
    if response_tax['status'] == 1000:
      response_tax['command'] = 'player_tax'
      self.send_response(response_tax)
    end_response = WebsocketService().end(game_id=content['game'].id, user_id=content['user'].id)
    if end_response['status']==1000:
      end_response['command'] = 'player_end'
      self.send_response(end_response, broadcast=False)
      end_response['command'] = 'board_end'
      self.send_response(end_response)

    response = WebsocketService().skip(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'player_skip'
    self.send_response(response)

  def move(self, content): #TODO: FIX
    response = WebsocketService().move(game_id=content['game'].id, user_id=content['user'].id)   
    response['command'] = 'board_move'
    self.send_response(response)
    if response['status'] != 2011:
      if response['status'] != 1997:
        response_offer_to_player = WebsocketService().offer(game_id=content['game'].id, user_id=content['user'].id)
        response_offer_to_player['command'] = 'player_offer'
        if response_offer_to_player['status']==1000:
          self.send_response(response_offer_to_player, broadcast=False)
        
        response['command'] = 'player_move'
        self.send_response(response, broadcast=False)
        
        response_chance_card = WebsocketService().chance(game_id=content['game'].id, user_id=content['user'].id)
        
        if response_chance_card['status']==1000:
          response_chance_card['command'] = 'player_chance'
          self.send_response(response_chance_card, broadcast=False)
          #self.join(content)

      else:
        response = WebsocketService().check(content['game'].id, content['user'].id)
        response['command'] = 'player_skip'
        self.send_response(response)


  def buy(self, content):
    response = WebsocketService().buy(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'player_join'
    if response['status']==1000:
      self.send_response(response, broadcast=False)
      response['command'] = 'board_join'
      self.send_response(response)

  def buy_building(self, content):
    response = WebsocketService().buy_building(game_id=content['game'].id, user_id=content['user'].id)
    response['command'] = 'board_building_update'
    self.send_response(response)
    response['command'] = 'player_join'
    self.send_response(response, broadcast=False)

  def sell_building(self, content):
    response = WebsocketService().sell_building(game_id=content['game'].id, user_id=content['user'].id, card_id=content['card_id'])
    response['command'] = 'board_building_update'
    self.send_response(response)
    response['command'] = 'player_join'
    self.send_response(response, broadcast=False)

  def deposit(self, content):
    response = WebsocketService().deposit(game_id=content['game'].id, user_id=content['user'].id, card_id=content['card_id'])
    response['command'] = 'board_building_update'
    self.send_response(response)
    response['command'] = 'player_join'
    self.send_response(response, broadcast=False)

  def buyback(self, content):
    response = WebsocketService().repurchase(game_id=content['game'].id, user_id=content['user'].id, card_id=content['card_id'])
    response['command'] = 'board_building_update'
    self.send_response(response)
    response['command'] = 'player_join'
    self.send_response(response, broadcast=False)

  def sell_property(self, content):
    response = WebsocketService().create_offer(game_id=content['game'].id, user_id=content['user'].id, card_id=content['card_id'], price=content['price'])
    response['command'] = 'player_resell_offer'
    self.send_response(response)

  def rebuy_property(self, content):
    response = WebsocketService().accept_offer(game_id=content['game'].id, user_id=content['user'].id, card_id=content['card_id'])
    response['command'] = 'player_resell_update'
    self.send_response(response)

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      self.__get_game(),
      self.channel_name,
    )
    self.send_json({
      "command": "disconnect",
      "response": "disconnected"        
    })


  def send_response(self, response, broadcast=True):
    if(broadcast):
      async_to_sync(self.channel_layer.group_send)(
      self.__get_game(),
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
  
  def __get_game(self):
    return self.scope["url_route"]["kwargs"]["game_id"]
  
  def __get_code(self):
    return self.scope["url_route"]["kwargs"]["code"]