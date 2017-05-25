from django.shortcuts import render, redirect
from django.contrib import messages
from models import *

# Create your views here.
def index(request):
    return render(request, 'login_and_registration/index.html')


def register(request):
    if request.POST:
        checker = User.objects.isValid(request.POST)
        print checker
        if checker['pass']==True:
            user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], password_confirmation=request.POST['password_confirmation'])

            context={
            'name': User.objects.filter(email=request.POST['email']).first().first_name
            }
            return render(request, 'login_and_registration/success.html', context)
        context={'errors': checker['errors']}
        return render(request, 'login_and_registration/index.html', context)
    else:
        return redirect('/')



def login(request):
    if request.POST:
        logger = User.objects.logging_in(request.POST)
        if logger['pass']==True:
            context={
                'name': User.objects.filter(email=request.POST['email']).first().first_name,
            }
            return render(request, 'login_and_registration/success.html', context)
        else:
            data={
                'errors_login': logger['errors']
            }
            return render(request, 'login_and_registration/index.html', data)


def logout(request):
    if request.POST:
        request.session.clear()
        return redirect('/')
