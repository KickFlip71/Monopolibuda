from game.models import Player
from game.providers import PlayerProvider
from random import randint


class PositionService:
	def __init__(self):
		self.status = 1000
		
	def move_player(self, game_id, user_id):
		self.status = 1004
		player = PlayerProvider().get_player(game_id, user_id)
		if player != None:# and player.move == 2:
			rolled_dice = randint(1,6)
			player.position += rolled_dice
			if player.position > 24:
				self.update_balance(player)
			player.position = player.position % 24
			self.disable_move(player)
			player.save()	
		return player, self.status

	def update_balance(self, player):
		money = 100
		player.balance += money
		return player

	def disable_move(self, player):
		player.move=1
		return player

	def __player_exists(self, player):
		result = player != None
		if not result:
			self.status = 2002
		return result


	def __players_turn(self, player):
		result = player.move == 2
		if not result:
			self.status = 2011
		return result