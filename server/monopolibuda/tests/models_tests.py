from game.models import Game, User, Card, Property, Player, Chance, Charge
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
from tests.factories.charge_factory import ChargeFactory
import pytest

@pytest.fixture
def valid_player(active=True, balance=500, move=0, position=0, game=None, user=None):
    if user == None:
      valid_user = UserFactory()
    else:
      valid_user = user
    
    if game == None:
      valid_game = GameFactory(active=True)
    else:
      valid_game = game
    return PlayerFactory(game=valid_game, user=valid_user, active=active, balance=balance, move=move, position=position)

@pytest.fixture
def valid_game(active=True, code=""):
    user = UserFactory()
    return Game(players_amount=4, host=user, active=active, code=code)

@pytest.fixture
def valid_property(player=None, buildings=0, deposited=False, selling_price=0):
    if player == None:
      owner = valid_player()
    else:
      owner = player
    return PropertyFactory(player=owner, buildings=buildings, deposited=deposited, selling_price=selling_price)

@pytest.mark.django_db(transaction=True)
def test_game_save_method_when_empty_code():
    game = valid_game()
    game.save()
    assert game.code != None

@pytest.mark.django_db(transaction=True)
def test_game_save_method_doesnt_change_code():
    game = valid_game(code="CODE")
    game.save()
    assert game.code == "CODE"

@pytest.mark.django_db(transaction=True)
def test_game_set_active_method():
    game = valid_game(active=False)
    game.set_active()
    assert game.active == True

@pytest.mark.django_db(transaction=True)
def test_player_defeat_method():
    player = valid_player()
    player.defeat()
    assert player.active == False

@pytest.mark.django_db(transaction=True)
def test_player_update_balance_method():
    player = valid_player()
    player.update_balance(500)
    assert player.balance == 1000

@pytest.mark.django_db(transaction=True)
def test_player_reset_balance_method():
    player = valid_player()
    player.reset_balance()
    assert player.balance == 0

@pytest.mark.django_db(transaction=True)
def test_player_can_pay_tax_method():
    player = valid_player()
    can_pay = player.can_pay_tax(300)
    assert can_pay == True

@pytest.mark.django_db(transaction=True)
def test_player_can_pay_tax_method_when_cannot():
    player = valid_player()
    can_pay = player.can_pay_tax(600)
    assert can_pay == False

@pytest.mark.django_db(transaction=True)
def test_player_is_bankrupt_method():
    player = valid_player()
    is_bankrupt = player.is_bankrupt()
    assert is_bankrupt == False

@pytest.mark.django_db(transaction=True)
def test_player_is_bankrupt_method_when_is():
    player = valid_player(balance=-500)
    is_bankrupt = player.is_bankrupt()
    assert is_bankrupt == True

@pytest.mark.django_db(transaction=True)
def test_player_enable_move_method():
    player = valid_player()
    player.enable_move()
    assert player.move == 2

@pytest.mark.django_db(transaction=True)
def test_player_disable_move_method():
    player = valid_player(move=2)
    player.disable_move()
    assert player.move == 1

@pytest.mark.django_db(transaction=True)
def test_player_check_position_when_valid():
    player = valid_player()
    valid_pos = player.check_position()
    assert valid_pos == False

@pytest.mark.django_db(transaction=True)
def test_player_check_position_when_invalid():
    player = valid_player(position=50)
    valid_pos = player.check_position()
    assert valid_pos == True

@pytest.mark.django_db(transaction=True)
def test_player_fix_position():
    player = valid_player(position=26)
    player.fix_position()
    assert player.position == 2

@pytest.mark.django_db(transaction=True)
def test_charge_for_one():
    charge = ChargeFactory()
    for_one = charge.get_charge_for_amount_of_buildings(1)
    assert for_one == charge.one_apartments

@pytest.mark.django_db(transaction=True)
def test_charge_for_three():
    charge = ChargeFactory()
    for_three = charge.get_charge_for_amount_of_buildings(3)
    assert for_three == charge.three_apartments


@pytest.mark.django_db(transaction=True)
def test_property_change_owner_method():
    user1 = UserFactory()
    game = GameFactory(host=user1)
    old_owner = valid_player(user=user1, game=game)
    new_owner = valid_player(game=game)
    player_property = valid_property(player=old_owner, selling_price=300)
    player_property.change_owner(new_owner, old_owner)
    assert player_property.player_id == new_owner.id
    assert old_owner.balance == 800
    assert new_owner.balance == 200

@pytest.mark.django_db(transaction=True)
def test_property_for_sell_method():
    player_property = valid_property(selling_price=0)
    player_property.for_sell(300)
    assert player_property.selling_price == 300

@pytest.mark.django_db(transaction=True)
def test_property_cancel_offer_method():
    player_property = valid_property(selling_price=500)
    player_property.cancel_offer()
    assert player_property.selling_price == 0

