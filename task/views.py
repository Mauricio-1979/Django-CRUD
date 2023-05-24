from django.shortcuts import render, redirect # redirigir pagina
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate  # crear cookie sesion al registrar user
from django.db import IntegrityError

# Create your views here.
def home(request):
    # return HttpResponse("<h1>Mi APP en Django</h1>")
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user) # Guarda la cookie sessionid en el browser
                return redirect('task')
            # except:   GNERIC EXCEPTION
            #     return render(request, 'signup.html', {
            #         'form': UserCreationForm,
            #         "error": "Username already exists"
            #     })
            except IntegrityError: # especific error
                return render(request, 'signup.html', {
                     'form': UserCreationForm,
                     "error": "Username already exists"
                    })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": "Password do not match"
                })

def task(request):
    return render(request, 'task.html')

# def task(request):
#     return render(request, 'base.html')

def signout(request):
    logout(request)
    return redirect('home')

def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('task')
        