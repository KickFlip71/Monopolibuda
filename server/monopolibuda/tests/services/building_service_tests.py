from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
from game.services.building_service import BuildingService
import pytest


@pytest.mark.django_db(transaction=True)
def test_buy_building_when_valid_buying_apartment():
    # GIVEN
    player = PlayerFactory(balance=500, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=0)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    new_balance = Player.objects.get(pk=player.id).balance    
    assert status == 1000
    assert property.buildings == 1
    assert new_balance == 0

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_valid_buying_hotel():
    # GIVEN
    player = PlayerFactory(balance=700, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=4)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    new_balance = Player.objects.get(pk=player.id).balance
    assert status == 1000
    assert property.buildings == 5
    assert new_balance == 0

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_player_cannot_afford():
    # GIVEN
    player = PlayerFactory(balance=100, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2012

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_buildings_limit_reached():
    # GIVEN
    player = PlayerFactory(balance=5000, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=5)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2014

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_player_is_not_owner():
    # GIVEN
    player = PlayerFactory(balance=5000, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, game=player.game)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2004
