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

	def transfer_tax_between_players(self, game_id, user1_id, user2_id):
		# player1 pays tax to player2
		player1 = PlayerProvider().get_player(game_id=game_id, user_id=user1_id)
		player2 = PlayerProvider().get_player(game_id=game_id, user_id=user2_id)
		if self.__player_exists(player1) and self.__player_exists(player2):
			user2_properties = PropertyProvider().get_player_properties(game_id=game_id, player_id=player2.id)

			cards = []
			for prop in user2_properties:
				cards.append(prop.card)

			card = CardProvider().get_card_with_position(player1.position)

			if card in cards:
				charge = ChargeProvider().get_charge(card.charge_id)
				property = PropertyProvider().get_property(game_id=game_id, player_id=player2.id, card_id=card.id)
				tax_to_pay = charge.get_charge_for_amount_of_buildings(property.buildings)
			
				if player1.can_pay_tax(tax_to_pay):	
					player1.update_balance(-tax_to_pay)
					player2.update_balance(tax_to_pay)
				else:
					user1_properties = PropertyProvider().get_player_properties(game_id=game_id, player_id=player1.id)
					for prop in user1_properties:
						prop.delete()

					player2.update_balance(player1.balance)
					player1.reset_balance()
					player1.defeat()	

				self.status = 1000
				return [player1, player2], self.status
			else:
				self.status = 2004
				return [], self.status	
		else:
			return [], self.status

	def buy_property(self, game_id, user_id):
		player = PlayerProvider().get_player(game_id=game_id, user_id=user_id)
		if self.__player_exists(player):
			card = CardProvider().get_card_with_position(player.position)
			if not PropertyProvider().is_property_taken(game_id, card.id):
				self.status = 1000
				property = Property(player_id=player.id, game_id=player.game_id, card_id=card.id)
				property.save()
				return property, self.status
			else:
				self.status = 2001 #todo
		else:
			self.status = 2002
		return None, self.status

	def __player_exists(self, player):
		result = player != None
		if not result:
			self.status = 2002
		return result