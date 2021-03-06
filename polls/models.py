import datetime
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    question = models.CharField(verbose_name='Question', max_length=200)
    pub_date = models.DateTimeField(verbose_name='Published Date')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(verbose_name='Choice',max_length=200)
    votes = models.IntegerField(verbose_name='Votes', default=0)

    def __str__(self):
        return self.choice_text

