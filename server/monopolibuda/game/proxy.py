from game.models import Game

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Proxy:
    def __init__(self, *args, **kwargs):
        self.games = Game.objects.all()

    def load(self):
        self.games = Game.objects.all()

    def save(self):
        self.games.save()

    def get_game_with_game_id(self, game_id):
        for game in games:
            if game.id == game_id:
                return game
        return None

    def get_games_with_host_id(self, host_id):
        result = []
        for game in games:
            if game.host.id == host_id:
                result.append(game)
        return result