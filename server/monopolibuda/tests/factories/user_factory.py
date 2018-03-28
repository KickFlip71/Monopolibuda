import factory
from pytest_factoryboy import register
from game.models import User
from factory.django import DjangoModelFactory

@register
class UserFactory(DjangoModelFactory):
  class Meta:
    model = User

  username = factory.Sequence(lambda n: 'username{0}'.format(n))
  email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
