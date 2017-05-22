from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import *
import logging, json, operator
from datetime import datetime, time, timedelta
import pytz
from django.core.mail import EmailMessage
from django.db.models import Q

# Create your views here.
def login(request):
    """
    View method. Returns the login/register page
    """

    assert isinstance(request, HttpRequest)

    if request.method == "GET":
        return render(request, 'app/login.html', {'title':'Login'})