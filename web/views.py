from web.forms import RegistrationForm, LoginForm, CreateTicketForm, CreateCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from web.models import Ticket, Comment, TicketHistory
import json
from ticket_manager.settings import SITE_TITLE, SITE_LOGO_NAME
from django.core import serializers
from choices import *

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response('register.html',RequestContext(request, {'form': form}))
    else:
        form = RegistrationForm()
    return render_to_response('register.html',RequestContext(request, {'form': form}))


@csrf_protect
def login_view(request):
    if(request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return render_to_response('login.html', RequestContext(request, {'form': form, 'error': False}))
            else:
                return render_to_response('login.html', RequestContext(request, {'form': form, 'error': True}))
        else:
            return render_to_response('login.html', RequestContext(request, {'form': form}))
    else:
        form = LoginForm()
        return render_to_response('login.html', RequestContext(request, {'form': form}))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    tickets = Ticket.objects.all().order_by('-id')
    users = User.objects.all()
    return render_to_response('home.html', RequestContext(request, {'tickets': tickets, 'users':users}))

@login_required
def create_ticket(request):
    print request.POST
    if(request.method == 'POST'):
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            assignee = form.cleaned_data['assignee']
            reporter = User.objects.get(id=request.user.id)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if assignee:
                assignee = User.objects.get(username=form.cleaned_data['assignee'])
            else:
                assignee = None
            ticket = Ticket.create(title, description, category, priority, assignee, reporter, start_date, end_date)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))
    else:
        form = CreateTicketForm()
        return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))

@login_required
def get_tickets(request):
    tickets = serializers.serialize("json", Ticket.objects.all())
    return HttpResponse(json.dumps({'tickets': tickets}))

@login_required
def view_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.category = dict(CATEGORY_CHOICES)[ticket.category]
    ticket.priority = dict(PRIORITY_CHOICES)[ticket.priority]
    stri = '<select id="ticket_status" onchange=update_status("'+str(ticket.start_date)+'")>'
    for choice in STATUS_CHOICES:
        if ticket.status == choice[0]:
            stri = stri +  "<option value='"+choice[0]+"' selected>"+str(choice[1])+"</option>"
        else:
            stri = stri +  "<option value='"+choice[0]+"'>"+str(choice[1])+"</option>"
    stri= stri + "</select>"
    ticket.status =  stri
    comments = Comment.objects.filter(ticket=ticket_id).order_by('-id')
    history = TicketHistory.objects.filter(ticket=ticket_id).order_by('-id')
    form = CreateCommentForm()
    return render_to_response('view_ticket.html', RequestContext(request, {'ticket': ticket, 'comments': comments, 'history':history, 'form': form}))

@login_required
def modify_ticket(request, ticket_id):
    if(request.method == 'POST'):
        form = CreateTicketForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            assignee = form.cleaned_data['assignee']
            reporter = User.objects.get(id=request.user.id)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if assignee:
                assignee = User.objects.get(username=form.cleaned_data['assignee'])
            else:
                assignee = None
            ticket = Ticket.modify(ticket_id, title, description, category, priority, assignee, reporter, start_date, end_date)
            return HttpResponseRedirect('/ticket/%s'%ticket_id)
        else:
            return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))
    else:
        ticket = Ticket.objects.get(id=ticket_id)
        form = CreateTicketForm(initial={'title': ticket.title, 'assignee': ticket.assignee, 'description': ticket.description,
                                         'category': ticket.category, 'priority': ticket.priority,
                                         'status': ticket.status, 'start_date': ticket.start_date, 'end_date': ticket.end_date})
        return render_to_response('modify_ticket.html', RequestContext(request, {'ticket': ticket, 'form': form}))


@login_required
def comments(request):
    if request.method == 'GET':
        comments = serializers.serialize("json", Comment.objects.all())
        return HttpResponse(json.dumps({'comments': comments}))
    elif request.method == 'POST':
        text = request.POST['text']
        ticket = Ticket.objects.get(id=request.POST['ticket'])
        user = User.objects.get(id=request.user.id)
        comment = Comment.objects.create(text=text, ticket=ticket, user=user)
        return HttpResponseRedirect("/ticket/%s/"%ticket.id)

@login_required
def view_user(request, user_id):
    tickets = Ticket.objects.filter(assignee=user_id).order_by('-id')
    jira_user = User.objects.get(id=user_id)
    return render_to_response('view_user.html', RequestContext(request, {'jira_user': jira_user, 'tickets': tickets}))

@login_required
def update_ticket_status(request, ticket_id):
    status = request.GET['status']
    user = User.objects.get(id=request.user.id)
    ticket = Ticket.update_status(user, int(ticket_id), str(status))
    return HttpResponse(json.dumps({'data': '1'}))
