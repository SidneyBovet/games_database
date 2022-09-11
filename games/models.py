from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=200)
    own_date = models.IntegerField(default=2000)
    min_players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    duration = models.IntegerField(default=60)
    game_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    game_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    bgg_id = models.IntegerField(default=0)
    def __str__(self):
        return self.name + ' (' + str(self.min_players) + '-' + str(self.max_players) + ', ' + self.game_type.name + ', ' + str(self.duration) + ' min)'
