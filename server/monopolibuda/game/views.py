from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

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