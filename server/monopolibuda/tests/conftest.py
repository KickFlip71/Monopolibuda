import os
import django
from django.conf import settings
from pytest_factoryboy import register
from tests.factories.user_factory import UserFactory
from tests.factories.game_factory import GameFactory
# from tests.factories.player_factory import PlayerFactory

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.config.settings')


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = False
    django.setup()


register(UserFactory)
register(GameFactory)
# register(PlayerFactory)
