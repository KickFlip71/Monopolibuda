from game.services.trading_service import TradingService
from game.models import Game, Player, Property
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
import pytest


@pytest.mark.django_db(transaction=True)
def test_create_offer_when_valid():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, player=player, game=game)
    [prop, status] = TradingService().create_offer(game.id, user.id, card.position, 5000)
    # THEN
    assert prop == user_property
    assert status == 1000

@pytest.mark.django_db(transaction=True)
def test_create_offer_when_player_doesnt_own_property():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, game=game)
    [prop, status] = TradingService().create_offer(game.id, user.id, card.position, 5000)
    # THEN
    assert prop == None
    assert status == 2004

@pytest.mark.django_db(transaction=True)
def test_create_offer_when_player_not_found():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, player=player, game=game)
    [prop, status] = TradingService().create_offer(game.id, user.id, card.position, 5000)
    # THEN
    assert prop == None
    assert status == 2002

@pytest.mark.django_db(transaction=True)
def test_create_offer_when_property_is_not_present():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card)
    [prop, status] = TradingService().create_offer(game.id, user.id, card.position, 5000)
    # THEN
    assert prop == None
    assert status == 2007


@pytest.mark.django_db(transaction=True)
def test_accept_offer_when_valid():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game, balance=6000)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, game=game)
    [new_owner, status] = TradingService().accept_offer(game.id, user.id, card.position, 5000)
    # THEN
    assert new_owner == player
    assert status == 1000

@pytest.mark.django_db(transaction=True)
def test_accept_offer_when_valid():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game, balance=6000)
    card = CardFactory(position=5)
    old_owner = PlayerFactory(game=game, balance=1000)
    user_property = PropertyFactory(card=card, game=game, player=old_owner, selling_price=5000)
    [new_owner, status] = TradingService().accept_offer(game.id, user.id, card.position)
    old_owner_new_balance = Player.objects.get(pk=old_owner.id).balance
    # THEN
    assert new_owner.balance == 1000
    assert old_owner_new_balance == 6000

@pytest.mark.django_db(transaction=True)
def test_accept_offer_when_cannot_afford():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game, balance=4000)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, game=game, selling_price=5000)
    [new_owner, status] = TradingService().accept_offer(game.id, user.id, card.position)
    # THEN
    assert new_owner == None
    assert status == 2012

@pytest.mark.django_db(transaction=True)
def test_accept_offer_when_not_for_sale():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game, balance=4000)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, game=game, selling_price=0)
    [new_owner, status] = TradingService().accept_offer(game.id, user.id, card.position)
    # THEN
    assert new_owner == None
    assert status == 2013

@pytest.mark.django_db(transaction=True)
def test_cancel_offer_when_valid():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, player=player, game=game, selling_price=5000)
    [prop, status] = TradingService().cancel_offer(game.id, user.id, card.position)
    # THEN
    assert prop.selling_price == 0
    assert status == 1000

@pytest.mark.django_db(transaction=True)
def test_cancel_offer_when_already_not_for_sale():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, player=player, game=game)
    [prop, status] = TradingService().cancel_offer(game.id, user.id, card.position)
    # THEN
    assert prop == None
    assert status == 2013

@pytest.mark.django_db(transaction=True)
def test_cancel_offer_when_user_is_not_owner():
    # GIVEN
    user = UserFactory()
    # WHEN
    game = GameFactory()
    player = PlayerFactory(user=user, game=game)
    card = CardFactory(position=5)
    user_property = PropertyFactory(card=card, game=game, selling_price=4000)
    [prop, status] = TradingService().cancel_offer(game.id, user.id, card.position)
    # THEN
    property_price = Property.objects.get(pk=user_property.id).selling_price
    assert property_price == 4000
    assert prop == None
    assert status == 2004