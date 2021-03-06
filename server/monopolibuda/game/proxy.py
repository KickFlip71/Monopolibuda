from game.models import Game, Player, Property, User, Card, Chance, Charge
from django.forms.models import model_to_dict

from random import choice

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Proxy:
    def __init__(self, *args, **kwargs):
        self.games_dict={}
        self.players_dict={}
        self.propertys_dict={}
        self.users_dict={}
        self.cards_dict={}
        self.charges_dict={}
        self.chances_dict={}
        self.load(full=True)

    def load(self, full=False):
        self.games_dict = dict( (o.pk, o) for o in Game.objects.all())
        self.players_dict = dict( (o.pk, o) for o in Player.objects.all())
        self.propertys_dict = dict( (o.pk, o) for o in Property.objects.all())
        self.users_dict = dict( (o.pk, o) for o in User.objects.all())
        if full:
            self.cards_dict = dict( (o.pk, o) for o in Card.objects.all())
            self.charges_dict = dict( (o.pk, o) for o in Charge.objects.all())
            self.chances_dict = dict( (o.pk, o) for o in Chance.objects.all())

    def save(self):
        for game in self.games_dict.copy().values():
            game.save()
        for player in self.players_dict.copy().values():
            player.save()
        for proper in self.propertys_dict.copy().values():
            proper.save()
        self.load()

    def get_player(self, game_id, user_id):
        for pk,player in self.players_dict.items():
            if player.game_id == game_id and player.user_id == user_id:
                return player
        return None

    def get_active_game_players(self, game_id):
        result = []
        for pk,player in self.players_dict.items():
            if player.game_id == game_id and player.active:
                result.append(player)
        return result

    def get_active_game_players_with_order_gt(self, game_id, order):
        result = []
        for pk,player in self.players_dict.items():
            if player.game_id == game_id and player.active and player.order>order:
                result.append(player)
        return result

    def get_game_players(self, game_id):
        result = []
        for pk,player in self.players_dict.items():
            if player.game_id == game_id:
                result.append(player)
        return result

    def get_owner(self, property_id):
        return self.players_dict[self.propertys_dict[property_id].player_id]

    def get_player_properties(self, game_id, player_id):
        result = []
        for pk,proper in self.propertys_dict.items():
            if proper.game_id == game_id and proper.player_id==player_id:
                result.append(proper)
        return result

    def get_player_properties_with_player_id(self, player_id):
        result = []
        for pk,proper in self.propertys_dict.items():
            if proper.player_id==player_id:
                result.append(proper)
        return result
  
    def get_property(self, game_id, player_id, card_id):
        for pk,proper in self.propertys_dict.items():
            if proper.game_id == game_id and proper.player_id == player_id and proper.card_id == card_id:
                return proper
        return None

    def is_property_taken(self, game_id, card_id):
        for pk,proper in self.propertys_dict.items():
            if proper.game_id == game_id and proper.card_id == card_id:
                return True
        return False

    def get_property_with_card(self, game_id, card_id):
        for pk,proper in self.propertys_dict.items():
            if proper.game_id == game_id and proper.card_id == card_id:
                return proper
        return None
    
    def get_property_with_position(self, game_id, position):
        card_id = -1
        for pk,card in self.cards_dict.items():
            if card.position == position:
                card_id = pk
                break
        if card_id >= 0:
            for pk,proper in self.propertys_dict.items():
                if proper.game_id == game_id and proper.card_id == card_id:
                    return proper
        return None

    def get_card_with_position(self, position):
        for pk,card in self.cards_dict.items():
            if card.position == position:
                return card
        return None

    def get_charge(self, charge_id):
        return self.charges_dict[charge_id]

    def get_chance(self):
        return self.chances_dict[choice(list(self.chances_dict))]

    def get_serialized_chance(self, chance, many=False):
        if chance:
            chance = model_to_dict(chance)
            return chance
        return None

    def get_serialized_charge(self, charge, many=False):
        if charge:
            charge = model_to_dict(charge)
            return charge
        return None

    def get_serialized_card(self, card, many=False):
        if card:
            card = model_to_dict(card)
            card['charge']=self.get_serialized_charge(self.charges_dict[card['charge']])
            return card
        return None

    def get_serialized_property(self, property, many=False):
        if property:
            property = model_to_dict(property)
            property['card']=self.get_serialized_card(self.cards_dict[property['card']])
            return property
        return None
    
    def get_serialized_player(self, player, many=False):
        if player:
            if not many:
                player = model_to_dict(player)
                property_set = []
                for property in self.get_player_properties_with_player_id(player['id']):
                    property_set.append(self.get_serialized_property(property))
                player['property_set']=property_set
                return player
            
            result=[]
            for p in player:
                p = model_to_dict(p)
                property_set = []
                for property in self.get_player_properties_with_player_id(p['id']):
                    property_set.append(self.get_serialized_property(property))
                p['property_set']=property_set
                result.append(p)
            return result
        return None

    def get_serialized_game(self, game, many=False):
        if game:
            if not many:
                game = model_to_dict(game)
                player_set = []
                for player in self.get_game_players(game['id']):
                    player_set.append(self.get_serialized_player(player))
                game['player_set']=player_set
                return game
            
            result = []
            for g in game:
                g = model_to_dict(g)
                player_set = []
                for player in self.get_game_players(g['id']):
                    player_set.append(self.get_serialized_player(player))
                g['player_set']=player_set
                result.append(g)
            return result
        return None
