from game.models import Player
from game.providers import PlayerProvider
from tests.factories.player_factory import PlayerFactory
import pytest


@pytest.mark.django_db(transaction=True)
def test_player_service_returns_valid_player():
    # GIVEN
    player = PlayerFactory()
    # WHEN
    provided_player = PlayerProvider().get_player(user_id=player.user_id, game_id=player.game_id)
    # THEN
    assert provided_player == player

@pytest.mark.django_db(transaction=True)
def test_player_service_returns_valid_player_when_there_are_more_players():
    # GIVEN
    player1 = PlayerFactory()
    player2 = PlayerFactory(game_id=player1.game_id)
    player3 = PlayerFactory(game_id=player1.game_id)
    # WHEN
    provided_player = PlayerProvider().get_player(user_id=player1.user_id, game_id=player1.game_id)
    # THEN
    assert provided_player == player1
