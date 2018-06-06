from game.models import Game, Player
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.card_factory import CardFactory
from tests.factories.property_factory import PropertyFactory
from game.services.card_service import CardService
from game.proxy import Proxy
import pytest


@pytest.mark.django_db(transaction=True)
def test_get_available_card_to_buy():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    user = UserFactory()
    player = PlayerFactory(game_id=game.id,user_id=user.id,position=1)
    Proxy().load(full=True)
    # WHEN
    get_card = CardService().get_available_card_to_buy(game_id=game.id,user_id=user.id)
    # THEN
    assert get_card == (card,1000)

@pytest.mark.django_db(transaction=True)
def test_get_not_possible_to_buy_card():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=1)
    user = UserFactory()
    player = PlayerFactory(game_id=game.id,user_id=user.id,position=0)
    Proxy().load(full=True)
    # WHEN
    get_card = CardService().get_available_card_to_buy(game_id=game.id,user_id=user.id)
    # THEN
    assert get_card == (None,2005)

@pytest.mark.django_db(transaction=True)
def test_get_already_owned_card_to_buy():
    # GIVEN
    Proxy()
    game = GameFactory()
    card = CardFactory(position=99)
    property = PropertyFactory(game_id=game.id, card_id=card.id)
    user = UserFactory()
    player = PlayerFactory(game_id=game.id,user_id=user.id,position=99)
    Proxy().load(full=True)
    # WHEN
    get_card = CardService().get_available_card_to_buy(game_id=game.id,user_id=user.id)
    # THEN
    assert get_card == (None,2006)