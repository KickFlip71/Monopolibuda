from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.property_factory import PropertyFactory
from tests.factories.card_factory import CardFactory
from tests.factories.charge_factory import ChargeFactory
from game.services.property_service import PropertyService
from game.models import Property, Game, User, Player, Card, Chance, Charge
from game.providers import PlayerProvider, PropertyProvider, CardProvider, ChargeProvider
from game.proxy import Proxy

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
  Proxy()
  player = PlayerFactory(position=3, move=2, jailed=0)
  Proxy().load()
  # WHEN
  properties, status = PropertyService().get_player_properties(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert len(properties) == 0

@pytest.mark.django_db(transaction=True)
def test_get_player_properties():
  # GIVEN
  Proxy()
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop1 = PropertyFactory(player=player, game_id=player.game_id)
  Proxy().load()
  # WHEN
  properties, status = PropertyService().get_player_properties(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert len(properties) == 1

@pytest.mark.django_db(transaction=True)
def test_get_player_more_than_one_properties():
  # GIVEN
  Proxy()
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop1 = PropertyFactory(player=player, game_id=player.game_id)
  prop2 = PropertyFactory(player=player, game_id=player.game_id)
  Proxy().load()
  # WHEN
  properties, status = PropertyService().get_player_properties(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert len(properties) == 2


@pytest.mark.django_db(transaction=True)
def test_get_charge_for_buildings():
  # GIVEN
  Proxy()
  tax = 1200
  charge = ChargeFactory(one_apartments=tax)
  card = CardFactory(charge=charge)
  property = PropertyFactory(buildings=1,card=card)
  Proxy().load(full=True)
  # WHEN
  tax_to_pay = charge.get_charge_for_amount_of_buildings(property.buildings)
  # THEN
  assert tax_to_pay == tax

@pytest.mark.django_db(transaction=True)
def test_pay_tax():
  # GIVEN
  Proxy()
  tax = 600
  game = GameFactory(players_amount=2)
  player1 = PlayerFactory(game=game, position=1, balance=2000) 
  player2 = PlayerFactory(game=game, balance=3000)
  charge = ChargeFactory(one_apartments=tax)
  card = CardFactory(charge=charge)
  property = PropertyFactory(player=player2, game=game, card=card, buildings=1)
  Proxy().load(full=True)
  # WHEN
  record, status = PropertyService().pay_tax(game_id=player1.game_id, user_id=player1.user_id)
  # THEN
  p2 = PlayerProvider().get_player(game_id=game.id, user_id=player2.user_id)
  assert status == 1000
  assert record[0].balance == (player1.balance-tax) and record[1].balance == (player2.balance + tax)

@pytest.mark.django_db(transaction=True)
def test_buy_property_property_is_not_taken():
  # GIVEN
  Proxy()
  player = PlayerFactory(position=1)
  card = CardFactory(position=1)
  Proxy().load(full=True)
  # WHEN
  property, status = PropertyService().buy_property(game_id=player.game_id, user_id=player.user_id)
  # THEN
  assert property != None
  assert status == 1000

@pytest.mark.django_db(transaction=True)
def test_buy_property_property_is_taken():
  # GIVEN
  Proxy()
  game = GameFactory(players_amount=2)
  player1 = PlayerFactory(game=game, position=1)
  player2 = PlayerFactory(game=game)
  card = CardFactory(position=1)
  property2 = PropertyFactory(player=player2, game=game, card=card)
  Proxy().load(full=True)
  # WHEN
  retrieved_property, status = PropertyService().buy_property(game_id=game.id, user_id=player1.user_id)
  # THEN
  assert retrieved_property == None

