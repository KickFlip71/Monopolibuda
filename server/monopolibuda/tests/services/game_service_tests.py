from game.services.game_service import GameService
from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from game.providers import PlayerProvider, GameProvider
from game.proxy import Proxy
import pytest


@pytest.mark.django_db(transaction=True)
def test_add_game_sets_proper_players_amount():
    # GIVEN
    Proxy()
    user = UserFactory()
    Proxy().load(full=True)
    # WHEN
    new_game, _ = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert new_game.players_amount == 5

@pytest.mark.django_db(transaction=True)
def test_add_game_creates_new_game():
    # GIVEN
    Proxy()
    user = UserFactory()
    Proxy().load(full=True)
    # WHEN
    new_game, _ = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert len(Proxy().games_dict) == 1

@pytest.mark.django_db(transaction=True)
def test_add_game_creates_new_game_with_code():
    # GIVEN
    Proxy()
    user = UserFactory()
    Proxy().load(full=True)
    # WHEN
    new_game, _ = GameService().add_game(host_id=user.id, players_amount=5)
    # THEN
    assert GameProvider().get_game(new_game.id).code is not None


@pytest.mark.django_db(transaction=True)
def test_join_player_creates_new_player():
    # GIVEN
    Proxy()
    game = GameFactory()
    user = UserFactory()
    Proxy().load(full=True)
    # WHEN
    GameService().join_player(game_id=game.id, user_id=user.id)
    # THEN
    assert len(PlayerProvider().get_game_players(game.id)) == 1

@pytest.mark.django_db(transaction=True)
def test_join_player_does_not_create_new_player_if_already_on_board():
    # GIVEN
    Proxy()
    game = GameFactory()
    user = UserFactory()
    Proxy().load(full=True)
    GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().join_player(game_id=game.id, user_id=user.id)
    # THEN
    assert len(PlayerProvider().get_game_players(game.id)) == 1

@pytest.mark.django_db(transaction=True)
def test_join_player_does_not_create_new_player_if_board_is_full():
    # GIVEN
    Proxy()
    game = GameFactory()
    for i in range(4):
        user = UserFactory()
        Proxy().load(full=True)
        GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().join_player(game_id=game.id, user_id=user.id)
    # THEN
    assert len(PlayerProvider().get_game_players(game.id)) == 4

@pytest.mark.django_db(transaction=True)
def test_set_player_defeated_changes_active_to_false():
    # GIVEN
    Proxy()
    user = UserFactory()
    game = GameFactory()
    Proxy().load(full=True)
    player, _ = GameService().join_player(game_id=game.id, user_id=user.id)
    # WHEN
    GameService().set_player_defeated(user_id=user.id, game_id=game.id)
    # THEN
    assert PlayerProvider().get_player_with_id(player.id).active == False

@pytest.mark.django_db(transaction=True)
def test_get_game_returns_proper_player():
    # GIVEN
    Proxy()
    user = UserFactory()
    game = GameFactory()
    Proxy().load(full=True)
    # WHEN
    get_game = GameService().get_game(game.id)
    # THEN
    assert get_game == (game, 1000)

@pytest.mark.django_db(transaction=True)
def test_skip_turn_sets_player_move_to_zero():
    # GIVEN
    Proxy()
    player = PlayerFactory(move=1)
    player = PlayerFactory(move=0, game_id=player.game_id, order=1)
    Proxy().load(full=True)
    # WHEN
    GameService().skip_turn(game_id=player.game_id, user_id=player.user_id)
    # THEN
    assert PlayerProvider().get_player_with_id(player.id).move == 0

@pytest.mark.django_db(transaction=True)
def test_skip_turn_doestn_set_move_to_zero_if_move_eq_two():
    # GIVEN
    Proxy()
    player = PlayerFactory(move=2)
    Proxy().load(full=True)
    # WHEN
    GameService().skip_turn(game_id=player.game_id, user_id=player.user_id)
    # THEN
    assert PlayerProvider().get_player_with_id(player.id).move == 2