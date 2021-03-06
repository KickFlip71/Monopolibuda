from rest_framework import serializers
from game.models import User, Game, Player, Card, Property, Charge, Chance

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

class ChanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Chance
    fields = ('id', 'chance_type', 'description', 'value')

class ChargeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Charge
    fields = ('id', 'zero_apartments', 'one_apartments', 'two_apartments', 'three_apartments','four_apartments','five_apartments')

class CardSerializer(serializers.ModelSerializer):
  charge = ChargeSerializer()

  class Meta:
    model = Card
    fields = ('id', 'name', 'cost', 'apartment_cost', 'hotel_cost', 'deposit_value', 'charge', 'group_number', 'position')

class PropertySerializer(serializers.ModelSerializer):
  card = CardSerializer()

  class Meta:
    model = Property
    fields = ('id', 'player_id', 'buildings', 'deposited', 'card', 'selling_price')

class PlayerSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  property_set = PropertySerializer(many=True)

  class Meta:
    model = Player
    fields = ('id', 'user', 'balance', 'jailed', 'position', 'active', 'jail_free_card', 'move', 'property_set', 'order')

class GameSerializer(serializers.ModelSerializer):
  player_set = PlayerSerializer(many=True) 
  host = UserSerializer()

  class Meta:
    model = Game
    fields = ('id', 'host', 'players_amount', 'player_set', 'active')
    depth=3


