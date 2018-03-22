import factory
from pytest_factoryboy import register
from game.models import Game, User
from factory.django import DjangoModelFactory
from tests.factories.user_factory import UserFactory

@register
class GameFactory(DjangoModelFactory):
  class Meta:
    model = Game

  code = "QWERT" 
  players_amount = 5 
  host = factory.SubFactory(UserFactory) 