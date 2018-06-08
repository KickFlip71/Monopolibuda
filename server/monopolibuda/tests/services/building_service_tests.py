from game.models import Game, Player, Property
from game.proxy import Proxy
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
from game.services.building_service import BuildingService
from game.providers import PlayerProvider, PropertyProvider
import pytest

# VALID REQUESTS

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_valid_buying_apartment():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=500, position=3, move=1)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=0, deposited=False)
    Proxy().load(full=True)
    [player, status] = BuildingService().buy_building(player.game_id, player.user_id)
    new_balance = PlayerProvider().get_player_with_id(player.id).balance
    updated_property = PropertyProvider().get_property_with_id(property.id)
    assert status == 1000
    assert updated_property.buildings == 1
    assert new_balance == 0

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_valid_buying_hotel():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=700, position=3, move=1)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=4, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    new_balance = PlayerProvider().get_player_with_id(player.id).balance
    updated_property = PropertyProvider().get_property_with_id(property.id)
    assert status == 1000
    assert updated_property.buildings == 5
    assert new_balance == 0

@pytest.mark.django_db(transaction=True)
def test_sell_building_when_valid_selling_apartment():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=0, position=3, move=1)
    card = CardFactory(position=7)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=1, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().sell_building(player.game_id, player.user_id, card.id)
    new_balance = PlayerProvider().get_player_with_id(player.id).balance
    updated_property = PropertyProvider().get_property_with_id(property.id)
    assert status == 1000
    assert updated_property.buildings == 0
    assert new_balance == 500

@pytest.mark.django_db(transaction=True)
def test_sell_building_when_valid_selling_hotel():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=0, position=3, move=1)
    card = CardFactory(position=7)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=5, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().sell_building(player.game_id, player.user_id, card.id)
    new_balance = PlayerProvider().get_player_with_id(player.id).balance
    updated_property = PropertyProvider().get_property_with_id(property.id)
    assert status == 1000
    assert updated_property.buildings == 4
    assert new_balance == 700

# INVALID REQUESTS


@pytest.mark.django_db(transaction=True)
def test_buy_building_when_buildings_limit_reached():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=5000, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=5, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2014

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_player_is_not_owner():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=5000, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, game=player.game)
    Proxy().load(full=True)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_player_is_not_owner():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=5000, position=3, move=1)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, game=player.game, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_sell_building_when_player_is_not_owner():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=5000, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, game=player.game, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().sell_building(player.game_id, player.user_id, card.id)
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_minimum_buildings_limit_reached():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=5000, position=3)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=0, deposited=False)
    Proxy().load(full=True)
    [property, status] = BuildingService().sell_building(player.game_id, player.user_id, card.id)
    assert status == 2015

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_property_is_deposited():
    # GIVEN
    Proxy()
    player = PlayerFactory(position=3, move=1)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=0, deposited=True)
    Proxy().load(full=True)
    [property, status] = BuildingService().buy_building(player.game_id, player.user_id)
    assert status == 2016

@pytest.mark.django_db(transaction=True)
def test_sell_building_when_property_is_deposited():
    # GIVEN
    Proxy()
    player = PlayerFactory(balance=5000, position=3, move=1)
    card = CardFactory(position=3)
    property = PropertyFactory(card=card, player=player, game=player.game, buildings=1, deposited=True)
    Proxy().load(full=True)
    [property, status] = BuildingService().sell_building(player.game_id, player.user_id, card.id)
    assert status == 2016