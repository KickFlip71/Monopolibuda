import factory
from pytest_factoryboy import register
from factory.django import DjangoModelFactory
from tests.factories.charge_factory import ChargeFactory
from game.models import Property, Game, User, Player, Card, Chance, Charge


@register
class ChanceFactory(DjangoModelFactory):
  class Meta:
    model = Chance

  chance_type = 1
  description = "Masz bonus"
  value = 1500
