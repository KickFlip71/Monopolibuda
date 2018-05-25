from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login, logout
from . import views


urlpatterns = [
    path('', include('game.urls')),
    path('accounts/login/', login),
    path('accounts/logout/', logout),
    # path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls)
]
