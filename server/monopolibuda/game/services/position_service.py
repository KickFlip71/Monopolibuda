from game.models import Player
from game.providers import PlayerProvider
from random import randint


class PositionService:
	def __init__(self):
		self.status = 1000
		
	def move_player(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id, user_id)
		if self.__player_exists(player) and self.__players_turn(player):
			if self.__player_jailed(player):
				player = self.decrement_player_jail(player)
			else:
				player = self.change_player_position(player)
		return player, self.status

	def change_player_position(self, player):
		self.status = 1004
		rolled_dice = randint(1,7)
		player.position += rolled_dice
		if player.check_position():
			player.update_balance()
			player.fix_position()
		player.disable_move()
		player.save()	
		return player

	def decrement_player_jail(self, player):
		self.status = 1003
		player.jailed -= 1
		player.move = 0
		player.save()
		return player

	def move_player_to_jail(self, game_id, user_id):
		self.status = 1003
		player = PlayerProvider().get_player(game_id, user_id)
		if self.__player_exists(player):
			player.jailed = 3
			player.move = 0
			player.save()
		return player, self.status

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

	def __player_jailed(self, player):
		result = player.jailed != 0
		if not result:
			self.status = 2011
		return result