from game.services.board_service import BoardService
from game.models import Game
from tests.factories.user_factory import UserFactory
import pytest


@pytest.mark.django_db(transaction=True)
def test_new_board():
    new_board = BoardService().add_board(host_id=1,players_amount=5)
    assert new_board.players_amount == 5
    assert Game.objects.all().count() == 1

def test_factories(user_factory):
    assert isinstance(user_factory, UserFactory)