import factory
from pytest_factoryboy import register
from game.models import User

@register
class UserFactory(factory.Factory):
  class Meta:
    model = User
