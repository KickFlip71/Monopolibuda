from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider


class PropertyService:
	def __init__(self):
		self.status = 1000

	def get_player_properties(self, game_id, player_id):
		return PropertyProvider().get_player_properties(game_id=game_id, player_id=player_id)
