from django.contrib.auth import authenticate , login as django_login
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from hw.forms import LoginForm, RegisterForm
from hw.models import USER_PROFILE


def index(request):
    print request.GET.get("name","None")
    return render(request,'index.html')


def register(request):
    if request.method=='GET':
        registerform = RegisterForm()
        return render(request, 'register.html' , {'registerform':registerform})
    else:
        return render(request,'index.html')

def login(request):
    if request.method=='GET':
        loginform = LoginForm()
        return render(request, 'login.html' , {'loginform':loginform})
    else:
        loginform = LoginForm(data=request.POST)
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        profile = request.POST.get('profile',None)
        errors , loggedin = [], False
        user = authenticate(username=username, password=password)
        if user!=None and profile in [x for x,y in USER_PROFILE]:

            if user.is_active:
                django_login(request, user)
                loggedin = True
                return render(request, 'login.html', {'loggedin':loggedin,})
            else:
                errors.append("Your account has been disabled")

        if user==None:
            errors.append("Username and Password Does not Matched")
        if profile not in [x for x,y in USER_PROFILE]:
            errors.append("Unexpected profile")

        return render(request,'login.html', {'loginform':loginform,
                                             'errors':errors
                                             })


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