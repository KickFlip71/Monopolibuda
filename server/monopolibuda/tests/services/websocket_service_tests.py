from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from game.services.websocket_service import WebsocketService
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_join_when_success():
  player = PlayerFactory()
  response = WebsocketService().join(player.game_id, player.user_id)
  assert response['error'] == 1201

@pytest.mark.django_db(transaction=True)
def test_leave_player_when_success():
  player = PlayerFactory()
  response = WebsocketService().leave(player.game_id, player.user_id)
  assert response['error'] == 1202

@pytest.mark.django_db(transaction=True)
def test_skip_when_success():
  player = PlayerFactory(move=1)
  response = WebsocketService().skip(player.game_id, player.user_id)
  assert response['error'] == 1203

@pytest.mark.django_db(transaction=True)
def test_move_when_success():
  player = PlayerFactory(move=2)
  response = WebsocketService().move(player.game_id, player.user_id)
  assert response['error'] == 1204
