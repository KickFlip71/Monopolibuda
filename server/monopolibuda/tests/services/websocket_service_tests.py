from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.property_factory import PropertyFactory
from tests.factories.card_factory import CardFactory
from game.services.websocket_service import WebsocketService
import pytest
import pdb


# SUCCESS TESTS

@pytest.mark.django_db(transaction=True)
def test_join_when_success():
  player = PlayerFactory()
  response = WebsocketService().join(player.game_id, player.user_id)
  assert response['status'] == 1001

@pytest.mark.django_db(transaction=True)
def test_leave_player_when_success():
  player = PlayerFactory()
  response = WebsocketService().leave(player.game_id, player.user_id)
  assert response['status'] == 1002

@pytest.mark.django_db(transaction=True)
def test_skip_when_success():
  player = PlayerFactory(move=1)
  response = WebsocketService().skip(player.game_id, player.user_id)
  assert response['status'] == 1003

@pytest.mark.django_db(transaction=True)
def test_move_when_success():
  player = PlayerFactory(move=2)
  response = WebsocketService().move(player.game_id, player.user_id)
  assert response['status'] == 1004

@pytest.mark.django_db(transaction=True)
def test_offer_when_success():
  player = PlayerFactory(position=1)
  card = CardFactory(position=1)
  response = WebsocketService().offer(player.game_id, player.user_id)
  assert response['status'] == 1000
  
@pytest.mark.django_db(transaction=True)
def test_buy_when_success():
  player = PlayerFactory(position=1)
  card = CardFactory(position=1)
  response = WebsocketService().buy(player.game_id, player.user_id)
  assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)
def test_tax_when_success():
  game = GameFactory()
  player = PlayerFactory(game=game, position=1)
  card = CardFactory(position=1)
  property = PropertyFactory(player=player, game=game, card=card)
  response = WebsocketService().tax(player.game_id, player.user_id)
  assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)
def test_buy_building_when_success():
  player = PlayerFactory(position=3)
  card = CardFactory(position=3)
  property = PropertyFactory(player=player, game=player.game, card=card, buildings=2)
  response = WebsocketService().buy_building(player.game_id, player.user_id)
  assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)
def test_sell_building_when_success():
  player = PlayerFactory(position=3)
  card = CardFactory(position=7)
  property = PropertyFactory(player=player, game=player.game, card=card, buildings=2)
  response = WebsocketService().sell_building(player.game_id, player.user_id, card.position)
  assert response['status'] == 1000


# ERRORS TESTS

@pytest.mark.django_db(transaction=True)
def test_offer_when_card_is_owned():
  game = GameFactory()
  card = CardFactory(position=1)
  property = PropertyFactory(game_id=game.id,card_id=card.id)
  player = PlayerFactory(game_id=game.id,position=1)
  response = WebsocketService().offer(player.game_id, player.user_id)
  assert response['status'] == 2006

@pytest.mark.django_db(transaction=True)
def test_offer_when_card_not_exists():
  player = PlayerFactory(position=0)
  response = WebsocketService().offer(player.game_id, player.user_id)
  assert response['status'] == 2005

@pytest.mark.django_db(transaction=True)
def test_tax_no_card():
  player = PlayerFactory()
  response = WebsocketService().tax(player.game_id, player.user_id)
  assert response['status'] == 2004

@pytest.mark.django_db(transaction=True)
def test_tax_property_does_not_exists():
  player = PlayerFactory(position=1)
  card = CardFactory(position=1)
  response = WebsocketService().tax(player.game_id, player.user_id)
  assert response['status'] == 2007
