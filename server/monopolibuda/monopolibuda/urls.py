from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('', include('game.urls')),
    path('accounts/login/', login),
    path('accounts/logout/', logout),
    path('admin/', admin.site.urls)
]
