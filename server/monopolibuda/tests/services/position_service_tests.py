from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from game.services.position_service import PositionService
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_move_player_player_can_move():
	player = PlayerFactory(position=3, move=2)
	old_position = player.position
	player_changed_position, status = PositionService().move_player(game_id=player.game_id, user_id=player.user_id)
	assert old_position != player_changed_position.position


@pytest.mark.django_db(transaction=True)
def test_move_player_player_cannot_move():
	player = PlayerFactory(position=3, move=0)
	old_position = player.position
	player_changed_position, status = PositionService().move_player(player.game_id, player.user_id)
	assert old_position == player_changed_position.position

@pytest.mark.django_db(transaction=True)
def test_update_balance():
	player = PlayerFactory()
	old_balance = player.balance
	player_changed_balance = PositionService().update_balance(player)
	assert old_balance != player_changed_balance.balance

