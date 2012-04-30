from django.db import models
from datetime import datetime

class Poll(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()

    def is_ongoing(self):
        now = datetime.now()
        if self.start_date <= now and now <= self.deadline:
            return True
        else:
            return False

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
