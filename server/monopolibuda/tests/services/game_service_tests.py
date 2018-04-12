from game.services.game_service import GameService
from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
import pytest


@pytest.mark.django_db(transaction=True)
def test_add_game_sets_proper_players_amount():
    # GIVEN
    user = UserFactory()
    # WHEN
    new_game, _ = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert new_game.players_amount == 5

@pytest.mark.django_db(transaction=True)
def test_add_game_creates_new_game():
    # GIVEN
    user = UserFactory()
    # WHEN
    new_game, _ = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert Game.objects.all().count() == 1


@pytest.mark.django_db(transaction=True)
def test_join_player_creates_new_player():
    # GIVEN
    game = GameFactory()
    user = UserFactory()
    # WHEN
    GameService().join_player(game_id=game.id, user_id=user.id)
    # THEN
    assert Player.objects.filter(game=game).count() == 1

@pytest.mark.django_db(transaction=True)
def test_join_player_does_not_create_new_player_if_already_on_board():
    # GIVEN
    game = GameFactory()
    user = UserFactory()
    GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().join_player(game_id=game.id, user_id=user.id)
    # THEN
    assert Player.objects.filter(game=game).count() == 1

@pytest.mark.django_db(transaction=True)
def test_join_player_does_not_create_new_player_if_board_is_full():
    # GIVEN
    game = GameFactory()
    for i in range(4):
        user = UserFactory()
        GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().join_player(game_id=game.id, user_id=user.id)
    # THEN
    assert Player.objects.filter(game=game).count() == 4

@pytest.mark.django_db(transaction=True)
def test_set_player_defeated_changes_active_to_false():
    # GIVEN
    user = UserFactory()
    game = GameFactory()
    player, _ = GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().set_player_defeated(user_id=user.id, game_id=game.id)
    # THEN
    assert Player.objects.get(pk=player.id).active == False

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
    player = GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().remove_player(game_id=game.id, user_id=user.id)
    # THEN
    assert len(Player.objects.filter(game=game)) == 0

@pytest.mark.django_db(transaction=True)
def test_skip_turn_sets_player_move_to_zero():
    # GIVEN
    player = PlayerFactory(move=1)
    player = PlayerFactory(move=0, game_id=player.game_id, order=1)
    # WHEN
    GameService().skip_turn(game_id=player.game_id, user_id=player.user_id)
    # THEN
    assert Player.objects.get(pk=player.id).move == 0

@pytest.mark.django_db(transaction=True)
def test_skip_turn_doestn_set_move_to_zero_if_move_eq_two():
    # GIVEN
    player = PlayerFactory(move=2)
    # WHEN
    GameService().skip_turn(game_id=player.game_id, user_id=player.user_id)
    # THEN
    assert Player.objects.get(pk=player.id).move == 2

def test_code_generator_returns_code_with_proper_length():
    # GIVEN
    code_length = 5
    # WHEN
    code = GameService().generate_code(code_length=code_length)
    # THEN
    assert len(code) == 5
