from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.property_factory import PropertyFactory
from tests.factories.card_factory import CardFactory
from tests.factories.charge_factory import ChargeFactory
from game.services.property_service import PropertyService
from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider

import pytest
import pdb

@pytest.mark.django_db(transaction=True)
def test_property_factory():
  # GIVEN
  player = PlayerFactory(position=3, move=2, jailed=0)
  # WHEN
  prop = PropertyFactory(player=player)
  # THEN
  assert prop.player_id == player.id

@pytest.mark.django_db(transaction=True)
def test_get_player_properties_no_property():
  # GIVEN
  player = PlayerFactory(position=3, move=2, jailed=0)
  # WHEN
  properties, status = PropertyService().get_player_properties(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert properties.count() == 0

@pytest.mark.django_db(transaction=True)
def test_get_player_properties():
  # GIVEN
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop1 = PropertyFactory(player=player, game_id=player.game_id)
  # WHEN
  properties, status = PropertyService().get_player_properties(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert properties.count() == 1

@pytest.mark.django_db(transaction=True)
def test_get_player_more_than_one_properties():
  # GIVEN
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop1 = PropertyFactory(player=player, game_id=player.game_id)
  prop2 = PropertyFactory(player=player, game_id=player.game_id)
  # WHEN
  properties, status = PropertyService().get_player_properties(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert properties.count() == 2


@pytest.mark.django_db(transaction=True)
def test_get_charge_for_buildings():
  # GIVEN
  tax = 1200
  charge = ChargeFactory(one_apartments=tax)
  card = CardFactory(charge=charge)
  property = PropertyFactory(buildings=1,card=card)
  # WHEN
  tax_to_pay = charge.get_charge_for_amount_of_buildings(property.buildings)
  # THEN
  assert tax_to_pay == tax

@pytest.mark.django_db(transaction=True)
def test_transfer_tax_between_players():
  # GIVEN
  tax = 600
  game = GameFactory(players_amount=2)
  player1 = PlayerFactory(game_id=game.id, position=1, balance=2000) 
  player2 = PlayerFactory(game_id=game.id, balance=3000)
  charge = ChargeFactory(one_apartments=tax)
  card = CardFactory(charge=charge)
  property = PropertyFactory(player=player2,game_id=game.id,card=card, buildings=1)
  # WHEN
  players, status = PropertyService().transfer_tax_between_players(game_id=player1.game_id, user1_id=player1.user_id, user2_id=player2.user_id)
  # THEN
  assert status == 1000
  assert len(players) == 2
  assert players[0].balance == (player1.balance-tax) and players[1].balance == (player2.balance + tax)

@pytest.mark.django_db(transaction=True)
def test_transfer_tax_between_players_fails_player_does_not_have_enough_money():
  # GIVEN
  tax = 3300
  player1_balance = 1000
  game = GameFactory(players_amount=2)
  player1 = PlayerFactory(game_id=game.id, position=1, balance=player1_balance) 
  player2 = PlayerFactory(game_id=game.id, balance=3000)
  charge = ChargeFactory(one_apartments=tax)
  card = CardFactory(charge=charge, position=1)
  card_user1 = CardFactory(charge=charge, position=2)
  property = PropertyFactory(player=player2,game_id=game.id,card=card, buildings=1)
  property_user1 = PropertyFactory(player=player1,game_id=game.id,card=card_user1, buildings=1)
  # WHEN
  players, status = PropertyService().transfer_tax_between_players(game_id=player1.game_id, user1_id=player1.user_id, user2_id=player2.user_id)
  # THEN
  assert status == 1000
  assert len(players) == 2
  assert players[0].active == False
  assert players[0].balance == 0 and players[1].balance == (player2.balance + player1_balance)
  assert len(PropertyProvider().get_player_properties(game_id=game.id, player_id=player1.id)) == 0

@pytest.mark.django_db(transaction=True)
def test_buy_property_property_is_not_taken():
  # GIVEN
  player = PlayerFactory(position=1)
  card = CardFactory(position=1)
  # WHEN
  property, status = PropertyService().buy_property(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert property != None
  assert status == 1000

@pytest.mark.django_db(transaction=True)
def test_buy_property_property_is_taken():
  # GIVEN
  game = GameFactory(players_amount=2)
  player1 = PlayerFactory(game=game, position=1)
  player2 = PlayerFactory(game=game)
  card = CardFactory(position=1)
  property2 = PropertyFactory(player=player2, game=game, card=card)
  # WHEN
  retrieved_property, status = PropertyService().buy_property(game_id=game.id, user_id=player1.user_id)
  # THEN
  assert retrieved_property == None

