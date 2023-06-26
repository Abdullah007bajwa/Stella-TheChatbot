from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .chatbot.bot import reply, initialization
from .models import BotUsers
from .decorators import login_required, logged_in
from django.urls import reverse
import os


@logged_in
def start(requests):
    # requests.session['user_name'] = 'guest'
    dic = {
        'nav_items': [('About', 'about')]
    }
    return render(requests, 'home.html', dic)


def signup(requests):
    ip = requests.META['REMOTE_ADDR']
    email = requests.POST.get('email')
    key1 = requests.POST.get('key1')
    name = str(requests.POST.get('name'))
    key2 = requests.POST.get('key2')
    gender = requests.POST.get('gender', 'other')
    errors = problems_in_signup(email, key1, key2)    # any problem in sign-up by user
    if len(errors['prob']) != 0:
        return JsonResponse(errors)
    pfp = gender+'.png'
    user = BotUsers(name=name.title(), gender=gender, ipaddress=ip, password=key1, email=email, picture=pfp)
    user.save()
    print('user created')
    requests.session['user_id'] = user.id
    requests.session['user_email'] = user.email
    requests.session['user_name'] = user.name
    print('sessions set')
    return redirect('upload')


def signin(requests):
    email = requests.POST.get('email')
    key = requests.POST.get('key')
    errors = problems_in_signin(email, key)         # any problem in sign-in by user
    if len(errors['prob']) != 0:
        return JsonResponse(errors)
    user = BotUsers.nodes.get(email=email)
    requests.session['user_id'] = user.id
    requests.session['user_email'] = user.email
    requests.session['user_name'] = user.name
    print(
        requests.session['user_id'],
        requests.session['user_email'],
        requests.session['user_name']
    )
    return redirect('bot')


@login_required
def uploaded(requests):
    if requests.method == 'POST':
        print('pfp post')
        image = requests.FILES['file']
        user_email = str(requests.POST.get('email'))
        pfp = create_file_name(user_email)
        file_path = './stella/static/profile_pics/'+pfp
        with open(file_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        user = BotUsers.nodes.get(email=user_email)
        user.picture = pfp
        user.save()
        return redirect('bot')
    print('pfp get')
    user = BotUsers.nodes.get(email=requests.session['user_email'])
    details = {
        'nav_items': [
            ('About', '/about'),
            ('Skip', '/stella')
        ],
        'username': user.name,
        'email': user.email,
        'gender': user.gender,
    }
    return render(requests, 'upload.html', details)


@login_required
def stella(requests):
    user_email = requests.session.get('user_email')
    user_id = requests.session.get('user_id')
    user_name = requests.session.get('user_name')
    user = BotUsers.nodes.get_or_none(email=user_email)
    if user is None:
        print('not signed in')
        return redirect('home')
    initialization(user_name, user_id)
    print('bot initialized')
    dic = {
        'nav_items': [
            ('Update Pic', '/upload/'),
            ('About', '/about'),
            ('LogOut', '/logout')
        ],
        'username': user.name,
        'email': user.email,
        'gender': user.gender,
        'pfp': user.picture
    }
    return render(requests, 'main.html', dic)


def logout(requests):
    requests.session['user_id'] = None
    requests.session['user_email'] = None
    requests.session['user_name'] = None
    return redirect('home')


def about(requests):
    return HttpResponse('<h1>ABOUT</h1>')


@login_required
def process_message(requests):
    user_input = requests.POST.get('in')
    print(requests.POST)
    user = requests.session['user_id']
    response = reply(user_input, user)
    data = {
        'bot_response': response,
    }
    return JsonResponse(data)


def create_file_name(email):
    i = email.index('@')
    e1, e2 = email[:i], email[i + 1:]
    i = e2.index('.')
    e2 = e2[:i]
    return e1 + e2 + '.png'


def problems_in_signup(email, key1, key2):
    errors = {
        'prob': []
    }
    try:
        user = BotUsers.nodes.get(email=email)
        errors['prob'].append('Email already registered, try SignIn')
    except BotUsers.DoesNotExist:
        pass
    if key1 != key2:
        errors['prob'].append('Passwords do not match')
    return errors


def problems_in_signin(email, key):
    errors = {
        'prob': []
    }

    try:
        user = BotUsers.nodes.get(email=email)
    except BotUsers.DoesNotExist:
        errors['prob'].append('Email not registered')
    else:
        if user.password != key:
            errors['prob'].append('Incorrect Password!')
    finally:
        return errors
