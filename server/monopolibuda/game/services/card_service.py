from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider


class CardService:
    def __init__(self):
        self.status = 1000

    def get_available_card_to_buy(self, game_id, user_id):
        player = PlayerProvider().get_player(game_id,user_id)
        card = CardProvider().get_card_with_position(player.position)
        if card:
            if not PropertyProvider().check_if_exist(game_id,card.id):
                return card, self.status
            else:
                self.status = 2006
                return None, self.status
        self.status = 2005
        return None, self.status