from django.db import models

# Create your models here.
class Todo(models.Model):
    item = models.TextField(max_length=300)
    description = models.TextField(max_length=1000)
    done = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()


class GameOdds(models.Model):
    given_id = models.TextField(max_length=100)
    game_id = models.IntegerField()
    team = models.TextField(max_length=200)
    line = models.DecimalField(max_digits=6, decimal_places=2)
    book = models.TextField(max_length=50)
    home_team = models.TextField(max_length=200)
    away_team = models.TextField(max_length=200)
    start_time = models.DateTimeField()
    league = models.TextField(max_length=15)
    line_update = models.DateTimeField()
