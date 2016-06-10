"""ticket_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from web.views import (login_view, logout_view, register, 
                       register_success, home, create_ticket,
                       get_all_tickets, view_ticket)
 
urlpatterns = patterns('',
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^register/$', register),
    url(r'^register_success/$', register_success),
    url(r'^$', home),
    url(r'^create_ticket/$',create_ticket),
    url(r'^get_tickets/$',get_all_tickets),
    url(r'^ticket/(?P<ticket_id>\d+)/$', view_ticket),
)
