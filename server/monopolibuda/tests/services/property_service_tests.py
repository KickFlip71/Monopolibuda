from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.property_factory import PropertyFactory
from game.services.property_service import PropertyService
from game.models import Property, Game, User, Player, Card, Chance, Charge
import pytest
import pdb

@pytest.mark.django_db(transaction=True)
def test_property_factory():
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop = PropertyFactory(player=player)
  assert prop.player_id == player.id

@pytest.mark.django_db(transaction=True)
def test_get_player_properties_no_property():
  player = PlayerFactory(position=3, move=2, jailed=0)
  assert PropertyService().get_player_properties(game_id=player.game_id, player_id=player.id).count() == 0

@pytest.mark.django_db(transaction=True)
def test_get_player_properties():
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop1 = PropertyFactory(player=player, game_id=player.game_id)
  assert PropertyService().get_player_properties(game_id=player.game_id, player_id=player.id).count() == 1

@pytest.mark.django_db(transaction=True)
def test_get_player_more_than_one_properties():
  player = PlayerFactory(position=3, move=2, jailed=0)
  prop1 = PropertyFactory(player=player, game_id=player.game_id)
  prop2 = PropertyFactory(player=player, game_id=player.game_id)
  assert PropertyService().get_player_properties(game_id=player.game_id, player_id=player.id).count() == 2