from __future__ import division
from django.db import models
from datetime import datetime


class Poll(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()

    def status(self):
        now = datetime.now()
        if self.start_date > now:
            return 'PENDING'
        elif now > self.deadline:
            return 'FINISHED'
        else:
            return 'ONGOING'

    def __unicode__(self):
        return self.title


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        choices = self.poll.choice_set.all()
        total = 0
        for choice in choices:
            total += choice.votes
        if total == 0:
            return 0
        else:
            return (self.votes / total) * 100

    def __unicode__(self):
        return self.choice


class VoterChoice(models.Model):
    choice = models.ForeignKey(Choice)
    phone_number = models.CharField(max_length=20)
