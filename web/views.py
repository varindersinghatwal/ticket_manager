from web.forms import RegistrationForm, LoginForm, CreateTicketForm, CreateCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from web.models import Ticket, Comment
import json
from ticket_manager.settings import SITE_TITLE, SITE_LOGO_NAME
from django.core import serializers

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
            if assignee:
                assignee = User.objects.get(username=form.cleaned_data['assignee'])
            else:
                assignee = None
            ticket = Ticket.create(title, description, category, priority, assignee, reporter)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))
    else:
        form = CreateTicketForm()
        return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))

#@login_required
#def get_tickets(request):
#    tickets = Ticket.get_all()
#    rows = []
#    for ticket in tickets:
#        row = {}
#        row['title'] = ticket.title
#        row['description'] = ticket.description
#        row['category'] = ticket.category
#        row['priority'] = ticket.priority
#        row['assignee'] = ticket.assignee.first_name + ' ' + ticket.assignee.last_name
#        row['reporter'] = ticket.reporter.first_name + ' ' + ticket.reporter.last_name
#        rows.append(row)
#    return HttpResponse(json.dumps({'data': rows}))

@login_required
def get_tickets(request):
    tickets = serializers.serialize("json", Ticket.objects.all())
    return HttpResponse(json.dumps({'tickets': tickets}))

@login_required
def view_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    comments = Comment.objects.filter(ticket=ticket_id).order_by('-id')
    form = CreateCommentForm()
    return render_to_response('view_ticket.html', RequestContext(request, {'ticket': ticket, 'comments': comments, 'form': form}))

@login_required
def modify_ticket(request, ticket_id):
    if(request.method == 'POST'):
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            assignee = form.cleaned_data['assignee']
            reporter = User.objects.get(id=request.user.id)
            if assignee:
                assignee = User.objects.get(username=form.cleaned_data['assignee'])
            else:
                assignee = None
            ticket = Ticket.modify(ticket_id, title, description, category, priority, assignee, reporter)
            return HttpResponseRedirect('/ticket/%s'%ticket_id)
        else:
            return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))
    else:
        ticket = Ticket.objects.get(id=ticket_id)
        form = CreateTicketForm(initial={'title': ticket.title, 'assignee': ticket.assignee, 'description': ticket.description,
                                         'category': ticket.category, 'priority': ticket.priority,
                                         'status': ticket.status})
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
