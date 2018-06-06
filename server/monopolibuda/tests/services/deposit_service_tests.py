from game.models import Game, Player, Property
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
from game.services.deposit_service import DepositService
from game.providers import PlayerProvider, PropertyProvider
from game.proxy import Proxy
import pytest


# WHEN VALID

@pytest.mark.django_db(transaction=True)
def test_deposit_when_valid():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=False)
    Proxy().load(full=True)
    # WHEN
    deposit_player, status = DepositService().deposit(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    new_balance = PlayerProvider().get_player_with_id(player.id).balance
    new_property = PropertyProvider().get_property_with_id(user_property.id)
    assert new_property == user_property 
    assert status == 1000
    assert new_property.deposited == True
    assert new_balance == (player.balance + card.deposit_value)


@pytest.mark.django_db(transaction=True)
def test_repurchase_when_valid():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=True)
    Proxy().load(full=True)
    # WHEN
    deposit_property, status = DepositService().repurchase(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    new_balance = PlayerProvider().get_player_with_id(player.id).balance
    new_property = PropertyProvider().get_property_with_id(user_property.id)
    assert new_property == user_property 
    assert status == 1000
    assert new_property.deposited == False
    assert new_balance == (player.balance - card.deposit_value)


# WHEN INVALID

@pytest.mark.django_db(transaction=True)
def test_deposit_when_not_owner():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(card=card, game=game, deposited=False)
    Proxy().load(full=True)
    # WHEN
    deposit_property, status = DepositService().deposit(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_deposit_when_already_deposited():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(player=player, card=card, game=game)
    Proxy().load(full=True)
    # WHEN
    deposit_property, status = DepositService().deposit(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2016

@pytest.mark.django_db(transaction=True)
def test_repurchase_when_not_owner():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id,move=1)
    user_property = PropertyFactory(card=card, game=game, deposited=False)
    Proxy().load(full=True)
    # WHEN
    deposit_property, status = DepositService().repurchase(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_repurchase_when_already_deposited():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id,move=1)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=False)
    Proxy().load(full=True)
    # WHEN
    deposit_property, status = DepositService().repurchase(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2017
