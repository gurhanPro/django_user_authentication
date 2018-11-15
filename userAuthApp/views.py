from django.shortcuts import render
from userAuthApp.forms import UserForm, UserProfileInfoForm
# Create your views here.
#imports for userAuthentication
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required




def index(request):
    return render(request, 'userAuthApp/index.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # one to one relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'userAuthApp/registration.html' ,
                                    {'user_form':user_form,
                                    'profile_form':profile_form,
                                    'registered':registered})

@login_required
def special(request):
    return HttpResponse("you are logged in")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("account not active")

        else:
            print("some tried to login")
            print("username: {} and password {}".format(username,password))
            return HttpResponse("invalid username or password")

    return render(request,'userAuthApp/login.html')
