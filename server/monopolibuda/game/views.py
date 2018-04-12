from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    current_user = request.user

    return render(request, 'home/index.html', {
        "user": current_user,
    })

def board(request):
    return render(request, 'board.html')

@login_required
def client(request):
    current_user = request.user
    return render(request, 'client.html', {
        "user": current_user,
    })
