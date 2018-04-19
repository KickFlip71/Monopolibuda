import factory
from pytest_factoryboy import register
from factory.django import DjangoModelFactory
from game.models import Property, Game, User, Player, Card, Chance, Charge


@register
class ChargeFactory(DjangoModelFactory):
  class Meta:
    model = Charge

  zero_apartments = 100
  one_apartments = 150
  two_apartments = 200
  three_apartments = 250
  four_apartments = 300
  five_apartments = 500