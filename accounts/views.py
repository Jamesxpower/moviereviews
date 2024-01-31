from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import IntegrityError

# Create your views here.
def signupaccount(request):
    if request.method == 'GET':
        #return render(request=request, template_name='signupaccount.html', context={'form': UserCreationForm})
        return render(request=request, template_name='signupaccount.html', context={'form': UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'] )

                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request=request, template_name='signupaccount.html',
                              context={'form': UserCreateForm,
                                       'error': 'Username already taken. Choose new user name.'})

        else:
            return render(request=request, template_name='signupaccount.html',
                          context={'form': UserCreateForm, 'error': 'Passwords do not match'})

def loginaccount(request):
    if request.method == 'GET':
        return render(request=request, template_name='loginaccount.html', context={'form': AuthenticationForm})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request=request, template_name='loginaccount.html',
                          context={'form': AuthenticationForm,
                                   'error': 'username and password do not match.'})
        else:
            login(request, user)
            return redirect('home')

@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')


