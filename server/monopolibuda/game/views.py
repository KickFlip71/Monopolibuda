from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from game.models import Game
from game.services.game_service import GameService


@login_required
def index(request):
    current_user = request.user
    games = Game.objects.all()
    return render(request, 'home/index.html', {
        "user": current_user,
        "games": games,
        "error": request.GET.get('error', '')
    })

@login_required
def board(request, game_id):
    code = request.GET.get('code', '')
    game = Game.objects.get(pk=game_id)
    current_user = request.user

    if current_user.id == game.host.id or game.code == code:
        return render(request, 'board.html', {
            'game': game
        })        
    else:
        return redirect('/' + "?error=Code Invalid")

def new_game(request):
    code = request.GET.get('code', '')
    current_user = request.user
    players_amount = request.GET.get('players_amount', 4)
    game, status = GameService().add_game(host_id=current_user.id, players_amount=players_amount)
    success = str(status)[0] == '1'

    if success:
        game_id = str(game.id)
        return redirect('/board/'+game_id)
    else:
        return redirect('/' + "?error="+status)


@login_required
def client(request, game_id):
    current_user = request.user
    game = Game.objects.get(pk=game_id)
    return render(request, 'client.html', {
        "user": current_user,
        "game": game
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})