from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider


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

					charge = ChargeProvider().get_charge(card.charge_id)
					player2 = PlayerProvider().get_player(game_id=game_id, user_id=property.player.user_id)
					tax_to_pay = charge.get_charge_for_amount_of_buildings(property.buildings)
				
					if player.can_pay_tax(tax_to_pay):	
						player.update_balance(-tax_to_pay)
						player2.update_balance(tax_to_pay)
					else:
						player1_properties = PropertyProvider().get_player_properties(game_id=game_id, player_id=player.id)
						for prop in player1_properties:
							prop.delete()

						player2.update_balance(player.balance)
						player.reset_balance()
						player.defeat()	

					self.status = 1000
					return [player, player2], self.status
				else:
					self.status = 2007
					return [], self.status
			else:
				self.status = 2004
				return [], self.status	
		else:
			return [], self.status

	def buy_property(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
		if self.__player_exists(player):
			card = CardProvider().get_card_with_position(player.position)
			if card != None:
				if not PropertyProvider().is_property_taken(game_id, card.id):
					self.status = 1000
					property = Property(player_id=player.id, game_id=player.game_id, card_id=card.id)
					property.save()
					return property, self.status
				else:
					self.status = 2006
			else:
				self.status = 2005
		else:
			self.status = 2002
		return None, self.status

	def __player_exists(self, player):
		result = player != None
		if not result:
			self.status = 2002
		return result