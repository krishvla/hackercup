from django.db import models

# Create your models here.

class Teams(models.Model):
    team_name = models.CharField(max_length=200)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        params = {
            "team_name": self.team_name,
            'score':self.score,
        }
        return "{team_name} - {score}".format(**params)