from django.shortcuts import render
from django.http import HttpResponse
from games.models import Game

def index(request):
    return HttpResponse(Game.objects.all())