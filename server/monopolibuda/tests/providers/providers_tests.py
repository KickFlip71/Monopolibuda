from game.models import Player
from game.providers import PlayerProvider
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.property_factory import PropertyFactory
from game.providers import PropertyProvider
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
def test_card_provider_returns_valid_card():
    # GIVEN
    player = PlayerFactory()
    property = PropertyFactory(player=player, game_id=player.game_id)
    # WHEN
    provided_properties = PropertyProvider().get_player_properties(game_id=player.game_id, player_id=player.id)
    # THEN
    assert provided_properties.first() == property


@pytest.mark.django_db(transaction=True)
def test_card_provider_returns_valid_card_when_there_are_more_players():
    # GIVEN
    player = PlayerFactory()
    player2 = PlayerFactory(game_id=player.game_id, order=1)
    property = PropertyFactory(player=player, game_id=player.game_id)
    property2 = PropertyFactory(player=player, game_id=player2.game_id)
    # WHEN
    provided_properties = PropertyProvider().get_player_properties(game_id=player.game_id, player_id=player.id)
    # THEN
    assert provided_properties.first() == property

