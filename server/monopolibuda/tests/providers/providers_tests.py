from game.models import Player, Card, Charge, Property
from game.providers import PlayerProvider, CardProvider, ChargeProvider, PropertyProvider
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.property_factory import PropertyFactory
from tests.factories.card_factory import CardFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.game_factory import GameFactory
from game.proxy import Proxy
import pytest


@pytest.mark.django_db(transaction=True)
def test_player_provider_returns_valid_player():
    # GIVEN
    player = PlayerFactory()
    # WHEN
    provided_player = PlayerProvider().get_player(user_id=player.user_id, game_id=player.game_id)
    # THEN
    assert provided_player == player

@pytest.mark.django_db(transaction=True)
def test_player_provider_returns_valid_player_when_there_are_more_players():
    # GIVEN
    player1 = PlayerFactory()
    player2 = PlayerFactory(game_id=player1.game_id, order=1)
    player3 = PlayerFactory(game_id=player1.game_id, order=2)
    # WHEN
    provided_player = PlayerProvider().get_player(user_id=player1.user_id, game_id=player1.game_id)
    # THEN
    assert provided_player == player1


@pytest.mark.django_db(transaction=True)
def test_property_provider_returns_valid_property():
    # GIVEN
    Proxy()
    player = PlayerFactory()
    property = PropertyFactory(player=player, game_id=player.game_id)
    Proxy().load()
    # WHEN
    provided_properties = PropertyProvider().get_player_properties(game_id=player.game_id, player_id=player.id)
    # THEN
    assert provided_properties[0] == property


@pytest.mark.django_db(transaction=True)
def test_property_provider_returns_valid_property_when_there_are_more_players():
    # GIVEN
    Proxy()
    player = PlayerFactory()
    player2 = PlayerFactory(game_id=player.game_id, order=1)
    property = PropertyFactory(player=player, game_id=player.game_id)
    property2 = PropertyFactory(player=player, game_id=player2.game_id)
    Proxy().load()
    # WHEN
    provided_properties = PropertyProvider().get_player_properties(game_id=player.game_id, player_id=player.id)
    # THEN
    assert provided_properties[0] == property

@pytest.mark.django_db(transaction=True)
def test_is_property_taken_returns_false():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory()
    Proxy().load()
    # WHEN
    is_taken = PropertyProvider().is_property_taken(game_id=game.id, card_id=card.id)
    # THEN
    assert is_taken == False

@pytest.mark.django_db(transaction=True)
def test_is_property_taken_returns_true():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory()
    player = PlayerFactory(game_id=game.id)
    property = PropertyFactory(player=player, game_id=game.id, card_id=card.id)
    Proxy().load()
    # WHEN
    is_taken = PropertyProvider().is_property_taken(game_id=game.id, card_id=card.id)
    # THEN
    assert is_taken == True

@pytest.mark.django_db(transaction=True)
def test_property_provider_returns_if_property_with_card_id_exist():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory()
    property = PropertyFactory(game_id=game.id,card_id=card.id)
    Proxy().load()
    # WHEN
    if_exist = PropertyProvider().check_if_exist(game_id=game.id,card_id=card.id)
    # THEN
    assert if_exist == True

@pytest.mark.django_db(transaction=True)
def test_property_provider_returns_if_property_with_card_id_not_exist():
    # GIVEN
    Proxy()
    game = GameFactory()
    property = PropertyFactory(game_id=game.id,card_id=1)
    Proxy().load()
    # WHEN
    if_exist = PropertyProvider().check_if_exist(game_id=game.id,card_id=2)
    # THEN
    assert if_exist == False

@pytest.mark.django_db(transaction=True)
def test_property_provider_returns_if_property_with_card_id_not_exist_in_specified_game():
    # GIVEN
    Proxy()
    game = GameFactory()
    game2 = GameFactory()
    card = CardFactory()
    property = PropertyFactory(game_id=game2.id,card_id=card.id)
    Proxy().load()
    # WHEN
    if_exist = PropertyProvider().check_if_exist(game_id=game.id,card_id=card.id)
    # THEN
    assert if_exist == False

@pytest.mark.django_db(transaction=True)
def test_card_provider_returns_valid_card():
    # GIVEN
    Proxy()
    card = CardFactory()
    Proxy().load(full=True)
    # WHEN
    provided_card = CardProvider().get_card_with_position(1)
    # THEN
    assert provided_card == card

@pytest.mark.django_db(transaction=True)
def test_card_provider_returns_no_card():
    # GIVEN
    Proxy()
    card = CardFactory()
    Proxy().load(full=True)
    # WHEN
    provided_card = CardProvider().get_card_with_position(0)
    # THEN
    assert provided_card == None

@pytest.mark.django_db(transaction=True)
def test_card_provider_returns_valid_card_when_there_are_more_cards():
    # GIVEN
    Proxy()
    card = CardFactory()
    card2 = CardFactory(position=2)
    card4 = CardFactory(position=4)
    Proxy().load(full=True)
    # WHEN
    provided_card = CardProvider().get_card_with_position(2)
    # THEN
    assert provided_card == card2

@pytest.mark.django_db(transaction=True)
def test_charge_provider_returns_valid_charge():
    # GIVEN
    Proxy()
    charge = ChargeFactory(id=1)
    Proxy().load(full=True)
    # WHEN
    provided_charge = ChargeProvider().get_charge(1)
    # THEN
    assert provided_charge == charge

@pytest.mark.django_db(transaction=True)
def test_charge_provider_returns_valid_card_when_there_are_more_charges():
    # GIVEN
    Proxy()
    charge = ChargeFactory(id=1)
    charge2 = ChargeFactory(pk=2)
    charge4 = ChargeFactory(pk=4)
    Proxy().load(full=True)
    # WHEN
    provided_charge = ChargeProvider().get_charge(4)
    # THEN
    assert provided_charge == charge4