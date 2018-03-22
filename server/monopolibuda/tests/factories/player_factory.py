import factory
from pytest_factoryboy import register
from game.models import Game, User, Player
from factory.django import DjangoModelFactory
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory

@register
class PlayerFactory(DjangoModelFactory):
	class Meta:
		model = Player

	user=factory.SubFactory(UserFactory)
	game=factory.SubFactory(GameFactory)
	balance=3000
	jailed=0
	position=0
	active=True
	jail_free_card=False
	move=0