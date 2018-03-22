from game.services.board_service import BoardService
from game.models import Game
from tests.factories.user_factory import UserFactory
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_new_board_players_amount():
    user = UserFactory()
    new_board = BoardService().add_board(host_id=user, players_amount=5)
    assert new_board.players_amount == 5

@pytest.mark.django_db(transaction=True)
def test_new_board_create():
    user = UserFactory()
    new_board = BoardService().add_board(host_id=user, players_amount=5)
    assert Game.objects.all().count() == 1

def test_board_service_code():
    code = BoardService().generate_code(code_length=5)
    assert len(code) == 5