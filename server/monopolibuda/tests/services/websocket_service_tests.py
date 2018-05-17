from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.property_factory import PropertyFactory
from tests.factories.card_factory import CardFactory
from tests.factories.charge_factory import ChargeFactory
from game.services.websocket_service import WebsocketService
from game.providers import PlayerProvider
from game.models import Player
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
  player2 = PlayerFactory(game_id=player.game_id)
  response = WebsocketService().skip(player.game_id, player.user_id)
  assert response['status'] == 1003

@pytest.mark.django_db(transaction=True)
def test_skip_when_success_and_last_player():
  player = PlayerFactory(move=1)
  response = WebsocketService().skip(player.game_id, player.user_id)
  assert response['status'] == 1410

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
def test_tax_when_success():
  game = GameFactory()
  init_balance = 1000
  cost = 100
  player = PlayerFactory(game=game, position=1, balance=init_balance)
  player2 = PlayerFactory(game=game, balance=init_balance)
  charge = ChargeFactory(zero_apartments=cost)
  card = CardFactory(position=1, charge=charge)
  property = PropertyFactory(player=player2, game=game, card=card, buildings=0)
  response = WebsocketService().tax(player.game_id, player.user_id)
  assert Player.objects.get(pk=player.id).balance == init_balance-cost
  assert Player.objects.get(pk=player2.id).balance == init_balance+cost

@pytest.mark.django_db(transaction=True)
def test_deposit_when_valid():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=False)
    # WHEN
    response = WebsocketService().deposit(user_id=player.user.id, game_id=game.id, position=card.position)
    # THEN
    assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)
def test_repurchase_when_valid():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=True)
    # WHEN
    response = WebsocketService().repurchase(user_id=player.user.id, game_id=game.id, position=card.position)
    # THEN
    assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)    
def test_create_offer_when_success():
  user = UserFactory()
  game = GameFactory()
  player = PlayerFactory(user=user, game=game)
  card = CardFactory(position=5)
  user_property = PropertyFactory(card=card, player=player, game=game)
  response = WebsocketService().create_offer(player.game_id, player.user_id, position=card.position, price=5000)
  assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)
def test_accept_offer_when_success():
  user = UserFactory()
  game = GameFactory()
  player = PlayerFactory(user=user, game=game, balance=6000)
  card = CardFactory(position=5)
  old_owner = PlayerFactory(game=game, balance=1000)
  user_property = PropertyFactory(card=card, game=game, player=old_owner, selling_price=5000)
  response = WebsocketService().accept_offer(player.game_id, player.user_id, position=card.position)
  assert response['status'] == 1000

@pytest.mark.django_db(transaction=True)
def test_cancel_offer_when_success():
  # GIVEN
  user = UserFactory()
  # WHEN
  game = GameFactory()
  player = PlayerFactory(user=user, game=game)
  card = CardFactory(position=5)
  user_property = PropertyFactory(card=card, player=player, game=game, selling_price=5000)
  response = WebsocketService().cancel_offer(player.game_id, player.user_id, position=card.position)
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
