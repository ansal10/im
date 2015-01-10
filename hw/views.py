from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    print request.GET.get("name","None")
    return render(request,'index.html')


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request,'db.html', {'greetings': greetings})

def register(request):
    return render(request, 'register.html' , {'name':'Anas'})

def login(request):
    return render(request, 'login.html' , {'name':'Anas'})

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