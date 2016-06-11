from django.db import models
from django.contrib.auth.models import User
from choices import * 
import datetime


class Ticket(models.Model):
    reporter = models.ForeignKey(User, null=False, blank=True, related_name='reporter')
    assignee = models.ForeignKey(User, null=True, blank=True, related_name='assignee')
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, null=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, null=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, null=False, default='OP')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)

    @classmethod
    def create(cls, title, description, category, priority, assignee, reporter, start_date, end_date):
        ticket = cls(title=title,
                        description=description,
                        category=category,
                        priority=priority,
                        assignee=assignee,
                        reporter=reporter,
                        start_date=start_date,
                        end_date=end_date,
                        )
        ticket.save()
        history = TicketHistory(ticket=ticket,
                                user=reporter,
                                status=ticket.status)
        history.save()
        return ticket

    @classmethod
    def modify(cls, ticket_id, title, description, category, priority, assignee, reporter, start_date, end_date):
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.title = title
        ticket.description = description
        ticket.category = category
        ticket.priority = priority
        ticket.assignee = assignee
        ticket.reporter = reporter
        ticket.start_date = start_date
        ticket.end_date = end_date
        ticket.save()
        return ticket

    @classmethod
    def get_all(cls):
        return cls.objects.all()
   
    @classmethod
    def update_status(cls, user, ticket_id, status):
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.status = status
        ticket.save()
        history = TicketHistory(ticket=ticket,
                                user=user,
                                status=status)
        history.save()
        return ticket


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(null=True, blank=True)

class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(User)
    status = models.CharField(max_length=2, null=False, default='OP')
    udpate_time = models.DateTimeField(auto_now_add=True, null=False)
