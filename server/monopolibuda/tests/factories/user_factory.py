import factory
from pytest_factoryboy import register
from game.models import User
from factory.django import DjangoModelFactory

@register
class UserFactory(DjangoModelFactory):
  class Meta:
    model = User

  username = factory.Faker('first_name')
  email = factory.Faker('email')
