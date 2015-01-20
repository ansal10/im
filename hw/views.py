from django.contrib.auth import authenticate , login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from hw.homework.dashboard import  getProjectsForScholar
from hw.models import Profile, PROJECT_STATUS, Subject
from django.db.models import Q
import pdb
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from hw.forms import LoginForm, RegisterForm
from hw.models import USER_PROFILE
from homework import dashboard

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='GET':
        registerform = RegisterForm()
        return render(request, 'register.html' , {'registerform':registerform})
    else:
        errors, registered = [],False
        registerform = RegisterForm(data=request.POST)
        if registerform.is_valid():
            #check for unique mail
            if User.objects.filter(email=request.POST.get('email')).__len__()!=0:
                errors.append("Email is already registered")

            #check for unique username
            if User.objects.filter(username=request.POST.get('username')).__len__()!=0:
                errors.append("Username is already registered")

            if errors.__len__()==0:
                try:
                    user = User()
                    user.first_name = request.POST.get('fname')
                    user.last_name = request.POST.get('lname')
                    user.email = request.POST.get('email')
                    user.username = request.POST.get('username')
                    user.set_password(request.POST.get('password'))
                    user.is_superuser=False
                    if request.POST.get('profile') not in [x for x,y in USER_PROFILE]:
                        errors.append("Unexpected Profile")
                    else:
                        user.save()
                        Profile.objects.create(user = user)
                        user.profile.profile = request.get('profile')
                        user.profile.balance=0.0
                        user.profile.save()
                        user.save()
                        registered=True
                except Exception, e:
                    errors.append("Registration Failed , Please try again later")
        return render(request, 'register.html', {'registerform':registerform,
                                                 'registered':registered,
                                                 'errors':errors})


def login(request):
    if request.method=='GET':
        loginform = LoginForm()
        next = request.REQUEST.get('next',"")
        return render(request, 'login.html' , {'loginform':loginform,'next':next})
    else:
        loginform = LoginForm(data=request.POST)
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        profile = request.POST.get('profile',None)
        next = request.POST.get('next',"")
        errors , loggedin = [], False
        user = authenticate(username=username, password=password)
        if user!=None and user.profile.profile==profile:

            if user.is_active:
                django_login(request, user)
                loggedin = True
                request.session['user_id'] = user.id
                if next:
                    return HttpResponseRedirect(next)
                return render(request, 'login.html', {'loggedin':loggedin,})
            else:
                errors.append("Your account has been disabled")

        if user==None:
            errors.append("Username and Password Does not Matched")
        if user!=None and user.profile.profile!=profile:
            errors.append("Please check your Profile")

        return render(request,'login.html', {'loginform':loginform,
                                             'errors':errors,
                                             'next':next
                                             })


@login_required
def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    if user.profile.profile == 'SCHOLAR':
        projects = getProjectsForScholar(params = request.GET)
        return render(request, 'scholar_dashboard.html', {'PROJECT_STATUS':PROJECT_STATUS,
                                                          'subjects':Subject.objects.all(),
                                                          'next':next
        })


def logout(request):
    print request
    django_logout(request)
    return render(request, 'index.html', {})


@login_required
def recharge(request):
    datetime = "[[day]] [[month]] [[date]] [[year]] 23:18:06 GMT+0530"
    datetime=datetime.replace("[[day]]",request.GET.get('day',""))\
        .replace("[[month]]",request.GET.get('month',""))\
        .replace("[[date]]",request.GET.get('date',""))\
        .replace("[[year]]",request.GET.get('year',""))

    return render(request, 'recharge.html' , {
        'mobile':request.GET.get('mobile',None),
        'value':request.GET.get('value',None),
        'orderid':request.GET.get('orderid',None),
        'email':request.GET.get('email',None),
        'name':request.GET.get('name',None),
        'provider':request.GET.get('provider',None),
        'datetime':datetime
    })
    # mobile:mobilenumber
    # value:amount
    # orderid:orderid
    # email: mailid
    # name:emailName
    # datetime:"Sat Dec 06 2014 23:18:06 GMT+0530 "