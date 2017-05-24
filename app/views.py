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
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username = email, password = password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                
                if Answer.objects.filter(user = user).exists():
                    return redirect(reverse('results'))
                else:
                    return redirect(reverse('test'))

@login_required
def logout(request):
    assert isinstance(request, HttpRequest)
    
    auth.logout(request)

    return redirect(reverse('login'))

def register(request):
    """
    Handles a POST request from the login page's
    registration form. When done redirects to login page.
    """

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']

        # create_user(username, email, password)
        # but here we are keeping the email and username same
        user = User.objects.create_user(email, email, password)
        user.first_name = name
        user.save()

        return redirect(reverse('login'))


@login_required
def test(request):
    """
    View method. Returns the test page. If the user has already
    taken the test, then redirects to the results page
    """

    assert isinstance(request, HttpRequest)

    if Answer.objects.filter(user = request.user).exists():
        return redirect(reverse('results'))

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

@login_required
def save(request):
    """
    Saves user responses after the test. Handles a POST
    method from submitting the test form.
    """

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        for q in Question.objects.all():
            if "question-" + str(q.id) in request.POST:
                option_id = int(request.POST["question-" + str(q.id)])

                if option_id != -1:
                    option = Option.objects.get(id = option_id)
                    ans = Answer(user = request.user, question = q, option = option)
                    ans.save()

    return redirect(reverse('results'))

@login_required
def results(request):
    """
    If a user has already taken the test, then this is called,
    displays some statitics related to user responses
    """

    assert isinstance(request, HttpRequest)

    if request.method == "GET":
        results = {}
        results['total_tests'] = len(Question.objects.all())
        results['test_results'] = {}
        results['name'] = request.user.first_name
        sum = 0

        for case in VisionCase.objects.all():
            results['test_results'][case.title] = len(Answer.objects.filter(user = request.user).filter(option__case = case))
            sum += results['test_results'][case.title]
            print(case.title + " = " + str(len(Answer.objects.filter(user = request.user).filter(option__case = case))))

        results['undetermined_tests'] = results['total_tests'] - sum

        return render(request, 'app/results.html', {'title':'Results', 'results' : results})