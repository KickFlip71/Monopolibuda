from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from game.services.position_service import PositionService
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_move_player_player_can_move():
	player = PlayerFactory(position=3, move=2, jailed=0)
	old_position = player.position
	player_changed_position, status = PositionService().move_player(game_id=player.game_id, user_id=player.user_id)
	assert old_position != player_changed_position.position

@pytest.mark.django_db(transaction=True)
def test_move_player_to_jail():
	player = PlayerFactory(position=3, move=2)
	player, status = PositionService().move_player_to_jail(game_id=player.game_id, user_id=player.user_id)
	assert player.jailed == 3

@pytest.mark.django_db(transaction=True)
def test_player_in_jail_last_time():
	player = PlayerFactory(position=3, move=2, jailed=1)
	old_position = player.position
	player, status = PositionService().move_player(game_id=player.game_id, user_id=player.user_id)
	assert player.jailed == 0

@pytest.mark.django_db(transaction=True)
def test_player_decrement_jail():
	player = PlayerFactory(position=3, move=2, jailed=2)
	player, status = PositionService().move_player(game_id=player.game_id, user_id=player.user_id)
	assert player.jailed == 1

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
	player.update_balance(100)
	assert old_balance != player.balance

@pytest.mark.django_db(transaction=True)
def test_fix_position():
	player = PlayerFactory(position=26)
	player.fix_position()
	assert player.position == 2

