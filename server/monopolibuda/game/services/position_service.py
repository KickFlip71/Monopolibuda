from game.models import Player
from game.providers import PlayerProvider
from django.conf import settings
from game.utils import Dice

class PositionService:
	def __init__(self, dice=Dice()):
		self.status = 1000
		self.dice = dice
		
	def move_player(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id, user_id)
		if self.__player_exists(player) and self.__players_turn(player):
			if self.__player_jailed(player):
				self.decrement_player_jail(player)
			else:
				self.change_player_position(player)
				if self.__player_on_jail_position(player):
					self.__move_player_to_jail(player)
		return player, self.status

	def change_player_position(self, player):
		money = settings.DEFAULT_GAME_SETTINGS['start_bonus']
		self.status = 1004
		rolled_dice = self.dice.roll()
		player.position += rolled_dice
		if player.check_position():
			player.update_balance(money)
			player.fix_position()
		player.disable_move()
		#player.save()	
		#return player

	def decrement_player_jail(self, player):
		self.status = 1997
		player.jailed -= 1
		PlayerProvider().skip_turn(player.id)		
		#return player

	def __player_on_jail_position(self, player):
		return player.position == settings.DEFAULT_GAME_SETTINGS['go_to_jail_position']

	def __move_player_to_jail(self, player):
		self.status = 1997
		if self.__player_exists(player):
			player.jailed = settings.DEFAULT_GAME_SETTINGS['jail_turns']
			player.position = settings.DEFAULT_GAME_SETTINGS['jail_position']
			player.move = 0
			PlayerProvider().skip_turn(player.id)
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