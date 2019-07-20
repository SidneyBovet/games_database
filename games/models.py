from django.db import models

class Genre(models.Model):
    genre_name = models.CharField(max_length=200)
    def __str__(self):
        return self.genre_name

class Type(models.Model):
    type_name = models.CharField(max_length=200)
    def __str__(self):
        return self.type_name

class Game(models.Model):
    name = models.CharField(max_length=200)
    own_date = models.DateTimeField('date published')
    min_players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    game_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    game_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    def __str__(self):
        return self.name + ' (' + str(self.min_players) + '-' + str(self.max_players) + ')'
