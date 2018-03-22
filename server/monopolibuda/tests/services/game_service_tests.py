from game.services.board_service import BoardService
from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_new_board_players_amount():
    user = UserFactory()
    new_board = BoardService().add_board(host_id=user.id, players_amount=5)
    assert new_board.players_amount == 5

@pytest.mark.django_db(transaction=True)
def test_new_board_create():
    user = UserFactory()
    new_board = BoardService().add_board(host_id=user.id, players_amount=5)
    assert Game.objects.all().count() == 1

def test_board_service_code_generator():
    code = BoardService().generate_code(code_length=5)
    assert len(code) == 5

@pytest.mark.django_db(transaction=True)
def test_board_service_add_player():
    game = GameFactory()
    user = UserFactory()
    code = BoardService().add_player(game_id=game.id, user_id=user.id)
    assert Player.objects.all().count() == 1