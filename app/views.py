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


def test(request):
    """
    View method. Returns the login/register page
    """

    assert isinstance(request, HttpRequest)

    if request.method == "GET":
        # query questions and options, put it into a list of dict
        result = []

        for question in Question.objects.all():
            dict = {}
            dict['text'] = question.text
            dict['image'] = 'app/images/' + question.image
            dict['id'] = question.id
            dict['options'] = []

            for item in Option.objects.filter(question = question):
                opt = {}
                opt['option'] = item.option
                opt['id'] = item.id
                dict['options'].append(opt)

            result.append(dict)

        return render(request, 'app/test.html', {'title':'Test', 'questions' : result})

def save(request):
    """
    Saves user responses after the test. Handles a POST
    method from submitting the test form.
    """

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        # save user responses

        return results(request)

def results(request):
    """
    If a user has already taken the test, then this is called,
    displays some statitics related to user responses
    """

    assert isinstance(request, HttpRequest)

    if request.method == "GET":
        return render(request, 'app/results.html', {'title':'Results'})