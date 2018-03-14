from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    return render(request, 'base.html')

def board(request):
    return render(request, 'board.html')