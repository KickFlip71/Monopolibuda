from game.services.game_service import GameService
from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
import pytest
import pdb


@pytest.mark.django_db(transaction=True)
def test_add_game_sets_proper_players_amount():
    # GIVEN
    user = UserFactory()
    # WHEN
    new_game = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert new_game.players_amount == 5

@pytest.mark.django_db(transaction=True)
def test_add_game_creates_new_game():
    # GIVEN
    user = UserFactory()
    # WHEN
    new_game = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert Game.objects.all().count() == 1


@pytest.mark.django_db(transaction=True)
def test_add_player_creates_new_player():
    # GIVEN
    game = GameFactory()
    user = UserFactory()
    # WHEN
    GameService().add_player(game_id=game.id, user_id=user.id)
    # THEN
    assert Player.objects.all().count() == 1

@pytest.mark.django_db(transaction=True)
def test_set_player_defeated_changes_active_to_false():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player = GameService().add_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().set_player_defeated(player.id)
    # THEN
    assert Player.objects.get(pk=player.id).active == False

@pytest.mark.django_db(transaction=True)
def test_get_player_returns_proper_player():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player = GameService().add_player(game_id=game.id, user_id=user.id)
    # WHEN
    get_player = GameService().get_player(game.id, user.id)
    # THEN
    assert get_player == player

@pytest.mark.django_db(transaction=True)
def test_get_game_returns_proper_player():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    # WHEN
    get_game = GameService().get_game(game.id)
    # THEN
    assert get_game == game

@pytest.mark.django_db(transaction=True)
def test_remove_player_removes_player_from_game():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player = GameService().add_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().remove_player(game.id, user.id)
    # THEN
    assert len(Player.objects.filter(game=game)) == 0

def test_code_generator_returns_code_with_proper_length():
    # GIVEN
    code_length = 5
    # WHEN
    code = GameService().generate_code(code_length=code_length)
    # THEN
    assert len(code) == 5
