from game.services.board_service import BoardService
from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_add_board_sets_proper_players_amount():
    # GIVEN
    user = UserFactory()
    # WHEN
    new_board = BoardService().add_board(host_id=user.id, players_amount=5)
    # THEN
    assert new_board.players_amount == 5

@pytest.mark.django_db(transaction=True)
def test_add_board_creates_new_board():
    # GIVEN
    user = UserFactory()
    # WHEN
    new_board = BoardService().add_board(host_id=user.id, players_amount=5)
    # THEN
    assert Game.objects.all().count() == 1


@pytest.mark.django_db(transaction=True)
def test_add_player_creates_new_player():
    # GIVEN
    game = GameFactory()
    user = UserFactory()
    # WHEN
    BoardService().add_player(game_id=game.id, user_id=user.id)
    # THEN
    assert Player.objects.all().count() == 1

@pytest.mark.django_db(transaction=True)
def test_set_player_defeated_changes_active_to_false():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player = BoardService().add_player(game_id=game.id, user_id=user.id)
    # WHEN
    BoardService().set_player_defeated(player.id)
    # THEN
    assert Player.objects.get(pk=player.id).active == False

@pytest.mark.django_db(transaction=True)
def test_get_player_returns_proper_player():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player = BoardService().add_player(game_id=game.id, user_id=user.id)
    # WHEN
    get_player = BoardService().get_player(game.id, user.id)
    # THEN
    assert get_player == player

@pytest.mark.django_db(transaction=True)
def test_remove_player_removes_player_from_game():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player = BoardService().add_player(game_id=game.id, user_id=user.id)
    # WHEN
    BoardService().remove_player(game.id, user.id)
    # THEN
    assert len(Player.objects.filter(game=game)) == 0

def test_code_generator_returns_code_with_proper_length():
    # GIVEN
    code_length = 5
    # WHEN
    code = BoardService().generate_code(code_length=code_length)
    # THEN
    assert len(code) == 5
