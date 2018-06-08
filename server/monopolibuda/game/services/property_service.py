from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider
from game.proxy import Proxy


class PropertyService:
	def __init__(self):
		self.status = 1000

	def get_player_properties(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
		if self.__player_exists(player):
			self.status = 1000
			return PropertyProvider().get_player_properties(game_id=game_id, player_id=player.id), self.status
		return [], self.status


	def pay_tax(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
		if self.__player_exists(player):
			card = CardProvider().get_card_with_position(player.position)
			if card != None:
				if PropertyProvider().check_if_exist(game_id, card.id):
					property = PropertyProvider().get_property_with_card(game_id, card.id)
					if property.player.user_id != user_id:
						charge = ChargeProvider().get_charge(card.charge_id)
						player2 = PlayerProvider().get_player(game_id=game_id, user_id=property.player.user_id)
						tax_to_pay = charge.get_charge_for_amount_of_buildings(property.buildings)
						print('1p old balance: ' + str(player.balance))
						player.update_balance(-tax_to_pay)
						print('1p new balance: '+str(player.balance))
						print('2p old balance: '+str(player2.balance))
						player2.update_balance(tax_to_pay)
						print('2p new balance: '+str(player2.balance))
						self.status = 1000
						return [player,player2], self.status
					else:
						self.status = 2000
						return None, self.status
				else:
					self.status = 2007
					return None, self.status
			else:
				self.status = 2004
				return None, self.status	
		else:
			self.status = 2000
			return None, self.status


	def buy_property(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
		if self.__player_exists(player):
			card = CardProvider().get_card_with_position(player.position)
			if card != None:
				if not PropertyProvider().is_property_taken(game_id, card.id):
					self.status = 1000
					property = Property(player_id=player.id,game_id=player.game_id, card_id=card.id)
					Proxy().propertys_dict[property.id]=property
					player.update_balance(-card.cost)
					return player, self.status
				else:
					self.status = 2006
			else:
				self.status = 2005
		else:
			self.status = 2002
		return None, self.status

	def release_player_properties(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
		if self.__player_exists(player):
			player_properties = PropertyProvider().get_player_properties(game_id=game_id, player_id=player.id)
			player_properties.delete()
		return None, self.status

	def __player_exists(self, player):
		result = player != None
		if not result:
			self.status = 2002
		return result
		