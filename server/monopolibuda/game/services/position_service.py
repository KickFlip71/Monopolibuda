from game.models import Player
from random import randint


class PositionService:
	def change_position(self, player):
		if player.move == 2:
			rolled_dice = randint(1,6)
			player.position += rolled_dice
			if player.position > 24:
				player.balance += 1000
			player.position = player.position % 24
		player.save()	
		return player


