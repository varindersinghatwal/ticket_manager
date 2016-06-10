from web.forms import RegistrationForm, LoginForm, CreateTicketForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from web.models import MyUser, Ticket, Comment
import json
from ticket_manager.settings import SITE_TITLE, SITE_LOGO_NAME
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect('/register_success/')
        else:
            return render_to_response('register.html',RequestContext(request, {'form': form}))
    else:
        form = RegistrationForm()
    return render_to_response('register.html',RequestContext(request, {'form': form}))
 
def register_success(request):
    return render_to_response('register_success.html',)

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
    tickets = Ticket.objects.all()
    users = MyUser.objects.all()
    return render_to_response('home.html', RequestContext(request, {'user': request.user, 'tickets': tickets, 'users':users,}))

@login_required
def create_ticket(request):
    if(request.method == 'POST'):
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            assignee = form.cleaned_data['assignee']
            reporter = form.cleaned_data['reporter']
            ticket = Ticket.create(title, description, category, priority, assignee, reporter)
            print Ticket.get_all()
            return HttpResponseRedirect('/')
    else:
        form = CreateTicketForm()
        return render_to_response('ticket_form.html', RequestContext(request, {'form': form}))

@login_required
def get_all_tickets(request):
    tickets = Ticket.get_all()
    rows = []
    for ticket in tickets:
        row = {}
        row['title'] = ticket.title
        row['description'] = ticket.description
        row['category'] = ticket.category
        row['priority'] = ticket.priority
        row['assignee'] = ticket.assignee.first_name + ' ' + ticket.assignee.last_name
        row['reporter'] = ticket.reporter.first_name + ' ' + ticket.reporter.last_name
        rows.append(row)
    return HttpResponse(json.dumps({'data': rows}))


@login_required
def view_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    comments = Comment.objects.filter(ticket=ticket_id)
    return render_to_response('view_ticket.html', RequestContext(request, {'ticket': ticket, 'comments': comments}))
