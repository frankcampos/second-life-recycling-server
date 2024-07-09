from django.db import models
from .game import Game
from .gamer import Gamer

class Event(models.Model):
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  description = models.CharField(max_length=100)
  date = models.DateField()
  time = models.DateTimeField()
  organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)

  @property
  def joined(self):
    return self.__joined

  @joined.setter
  def joined(self, value):
    self.__joined = value
