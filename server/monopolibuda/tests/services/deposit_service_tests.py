from game.models import Game, Player, Property
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
from game.services.deposit_service import DepositService
import pytest


# WHEN VALID

@pytest.mark.django_db(transaction=True)
def test_deposit_when_valid():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=False)
    # WHEN
    deposit_player, status = DepositService().deposit(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    new_balance = Player.objects.get(pk=player.id).balance
    new_property = Property.objects.get(pk=user_property.id)
    assert new_property == user_property 
    assert status == 1000
    assert new_property.deposited == True
    assert new_balance == (player.balance + card.deposit_value)


@pytest.mark.django_db(transaction=True)
def test_repurchase_when_valid():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=True)
    # WHEN
    deposit_property, status = DepositService().repurchase(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    new_balance = Player.objects.get(pk=player.id).balance
    new_property = Property.objects.get(pk=user_property.id)
    assert new_property == user_property 
    assert status == 1000
    assert new_property.deposited == False
    assert new_balance == (player.balance - card.deposit_value)


# WHEN INVALID

@pytest.mark.django_db(transaction=True)
def test_deposit_when_not_owner():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(card=card, game=game, deposited=False)
    # WHEN
    deposit_property, status = DepositService().deposit(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_deposit_when_already_deposited():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id, move=1)
    user_property = PropertyFactory(player=player, card=card, game=game)
    # WHEN
    deposit_property, status = DepositService().deposit(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2016

@pytest.mark.django_db(transaction=True)
def test_repurchase_when_not_owner():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id,move=1)
    user_property = PropertyFactory(card=card, game=game, deposited=False)
    # WHEN
    deposit_property, status = DepositService().repurchase(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_repurchase_when_already_deposited():
    # GIVEN
    game = GameFactory()
    card = CardFactory(position=1)
    player = PlayerFactory(game_id=game.id,move=1)
    user_property = PropertyFactory(player=player, card=card, game=game, deposited=False)
    # WHEN
    deposit_property, status = DepositService().repurchase(user_id=player.user.id, game_id=game.id, card_id=card.id)
    # THEN
    assert deposit_property == None 
    assert status == 2017
