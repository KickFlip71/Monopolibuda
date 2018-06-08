from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.chance_factory import ChanceFactory
from game.services.chance_service import ChanceService
from game.providers import PlayerProvider
from game.proxy import Proxy
import pytest
from django.conf import settings
from game.models import Player

@pytest.mark.django_db(transaction=True)
def test_chance_add_value():
  Proxy()
  chance = ChanceFactory()
  player = PlayerFactory(balance=2500, position=3)
  Proxy().load(full=True)
  chance, status = ChanceService().get_chance_card(game_id=player.game.id, user_id=player.user.id)
  new_balance = PlayerProvider().get_player_with_id(player.id).balance
  assert new_balance == (player.balance + chance.value)

@pytest.mark.django_db(transaction=True)
def test_chance_add_minus_value():
  Proxy()
  chance = ChanceFactory(value=-1500)
  player = PlayerFactory(balance=2500, position=3)
  Proxy().load(full=True)
  chance, status = ChanceService().get_chance_card(game_id=player.game.id, user_id=player.user.id)
  new_balance = PlayerProvider().get_player_with_id(player.id).balance
  assert new_balance == (player.balance + chance.value)

@pytest.mark.django_db(transaction=True)
def test_chance_player_wrong_position():
  Proxy()
  chance = ChanceFactory(value=-1500)
  player = PlayerFactory(balance=2500, position=4)
  Proxy().load(full=True)
  chance, status = ChanceService().get_chance_card(game_id=player.game.id, user_id=player.user.id)
  assert 2018 == status