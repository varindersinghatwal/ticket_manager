from django.db import models
from django.contrib.auth.models import User
from choices import * 
import datetime

class MyUser(User):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)

class Ticket(models.Model):
    reporter = models.ForeignKey(User, null=False, related_name='reporter')
    assignee = models.ForeignKey(User, null=False, related_name='assignee')
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=1, null=False)
    priority = models.CharField(max_length=1, null=False)
    status = models.CharField(max_length=2, null=False, default='OP')
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create(cls, title, description, category, priority, assignee, reporter):
        ticket = cls(title=title,
                        description=description,
                        category=category,
                        priority=priority,
                        start_date=datetime.datetime.now(),
                        assignee=User.objects.get(id=assignee),
                        reporter=User.objects.get(id=reporter)
                        )
        ticket.save()
        return ticket

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(MyUser)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(null=True, blank=True)
