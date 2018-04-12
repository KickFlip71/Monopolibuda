import factory
from pytest_factoryboy import register
from factory.django import DjangoModelFactory
from tests.factories.charge_factory import ChargeFactory
from game.models import Property, Game, User, Player, Card, Chance, Charge


@register
class CardFactory(DjangoModelFactory):
  class Meta:
    model = Card

  name = "KARTA"
  cost = 100
  apartment_cost = 500
  hotel_cost = 700
  deposit_value = 500
  charge = factory.SubFactory(ChargeFactory)
  group_number = 0
  position = 1