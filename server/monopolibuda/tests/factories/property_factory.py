import factory
from pytest_factoryboy import register
from game.models import Game, Player, Card, Charge, Property
from factory.django import DjangoModelFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.game_factory import GameFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.card_factory import CardFactory


@register
class PropertyFactory(DjangoModelFactory):
  class Meta:
    model = Property

  player = factory.SubFactory(PlayerFactory)
  buildings = 2
  deposited = False
  game = factory.SubFactory(GameFactory)
  card = factory.SubFactory(CardFactory)