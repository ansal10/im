from django.contrib.auth import authenticate , login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from hw.homework.bid import applyBid, getBids, confirmBid, deleteBids
from hw.homework.getProjectDetails import getProjectDetailsForStudent, performActionOnProject, getEditableProject, \
    getProjectsForStudent, getProjectsForScholar
from hw.homework.helper import saveformtoProject, convertTimeToStr
from hw.models import Profile, PROJECT_STATUS, Subject, Bid, Project, BID_CHOICES
from django.db.models import Q
import pdb
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from hw.forms import LoginForm, RegisterForm, ProjectPostingForm, BidForm
from hw.models import USER_PROFILE
from homework import dashboard

def user_is_student(user):
    return True if user.profile.profile=='STUD' else False


def index(request, messages=[]):
    user=None
    if request.session.get('user_id',None):
        user = User.objects.get(id=request.session.get('user_id'))
    return render(request,'index.html', {
                                        'SESSION':request.session,
                                        'USER':user,
                                        'messages':messages
    })

def register(request):
    if request.session.get('loggedin',None):
        u = User.objects.get(id=request.session['user_id'])
        messages = ['Already Logged in as '+str(u.username)]
        return render(request, 'index.html', {'messages':messages,
                                              'SESSION':request.session
        })
    if request.method=='GET':
        registerform = RegisterForm()
        return render(request, 'register.html' , {'registerform':registerform})
    else:
        errors, registered = [],False
        registerform = RegisterForm(data=request.POST)
        if registerform.is_valid():
            #check for unique mail
            if User.objects.filter(email__iexact=request.POST.get('email')).__len__()!=0:
                errors.append("Email is already registered")

            #check for unique username
            if User.objects.filter(username__iexact=request.POST.get('username')).__len__()!=0:
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
                    user.is_active=True if request.POST.get('profile',None)=="STUD" else False
                    if request.POST.get('profile') not in [x for x,y in USER_PROFILE]:
                        errors.append("Unexpected Profile")
                    else:
                        user.save()
                        Profile.objects.create(user = user)
                        user.profile.profile = request.POST.get('profile')
                        user.profile.balance=0.0
                        user.profile.save()
                        user.save()
                        registered=True
                except Exception, e:
                    errors.append("Registration Failed , Please try again later")
        return render(request, 'register.html', {'registerform':registerform,
                                                 'registered':registered,
                                                 'errors':errors
        })


def login(request):

    if request.session.get('loggedin',None):
        u = User.objects.get(id=request.session['user_id'])
        messages = ['Already Logged in as '+str(u.username)]
        return render(request, 'index.html', {'messages':messages,
                                              'SESSION':request.session
        })

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
                request.session['loggedin']=True
                if next:
                    return HttpResponseRedirect(next)
                return index(request,messages=["Signed In Successfully"])
            else:
                errors.append("Your account has been disabled")

        if user==None:
            errors.append("Username and Password Does not Matched")
        if user!=None and user.profile.profile!=profile:
            errors.append("Please check your Profile")

        return render(request,'login.html', {'loginform':loginform,
                                             'errors':errors,
                                             'next':next,
                                             'SESSION':request.session
                                             })


@login_required
def dashboard(request, subject=None, project_id=None):
    user = User.objects.get(id=request.session['user_id'])
    if user.profile.profile == 'SCHOLAR':
        projects = getProjectsForScholar(subject=subject, project_id=project_id)
        if not project_id:
            # list all projects
            return render(request, 'scholar_dashboard/scholar_dashboard2.html', {'PROJECT_STATUS':PROJECT_STATUS,
                                                        'subjects':Subject.objects.filter(deleted_on=None).order_by('name'),
                                                          'next':next,
                                                          'SESSION':request.session,
                                                          'USER':user,
                                                          'projects':projects
            })
        else:
            #list details of project_id
            deletable,errors,messages=False,[],[]
            if request.method=='POST':
                errors = errors+applyBid(user_id=request.session['user_id'], project_id=project_id, bidform=BidForm(request.POST))
                bidform=BidForm(request.POST)
                if not errors:
                    messages.append("Suucessfully placed your bid")
                    deletable=True
                e, project, bids=getProjectDetailsForScholar(project_id=project_id)
            elif request.method=='GET':
                e, project, bids=getProjectDetailsForStudent(project_id=project_id)
                bid = Bid.objects.filter(project=project, user=user, deleted_on=None)
                if bid:
                    bidform = BidForm(data={'amount':bid[0].amount, 'deliver_by':convertTimeToStr(bid[0].deliever_by), 'description':bid[0].description})
                    deletable=True
                else:
                    bidform = BidForm()
                    deletable=False
            errors=errors+e

            return render(request, 'scholar_dashboard/project_details.html', {'PROJECT_STATUS':PROJECT_STATUS,
                                                          'subjects':Subject.objects.filter(deleted_on=None).order_by('name'),
                                                          'bidform':bidform,
                                                            'errors':errors,
                                                            'project':project,
                                                            'bids':bids,
                                                            'SESSION':request.session,
                                                            'USER':user,
                                                            'messages':messages,
                                                            'deletable':deletable
            })
    else:
        return HttpResponseRedirect('/projects')



@login_required
def bids(request):
    user = User.objects.get(id=request.session['user_id'])
    errors,bids = getBids(user_id=request.session.get('user_id',None))

    return render(request, 'scholar_dashboard/bids.html', {
                  'subjects':Subject.objects.filter(deleted_on=None).order_by('name'),
                  'errors':errors,
                  'SESSION':request.session,
                  'USER':user,
                  'BID_CHOICES':BID_CHOICES,
                  'bids':bids
    })


@login_required
@user_passes_test(user_is_student, login_url='/permission_denied')
def projects(request):
    user = User.objects.get(id=request.session['user_id'])
    if user.profile.profile == 'STUD':
        return render(request, 'stud_dashboard/stud_dashboard.html' , {
                                                        'SESSION':request.session,
                                                        'USER':user
        })
    else:
       return HttpResponseRedirect('/dashboard')


def logout(request):
    print request
    django_logout(request)
    message=['Logout Successfully']
    return render(request, 'index.html', {'messages':message,
                                          'SESSION':request.session
    })

@login_required
@user_passes_test(user_is_student, login_url='/permission_denied')
def newproject(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method=="GET":
        postprojectform = ProjectPostingForm()
        return render(request, 'stud_dashboard/new_project.html', {
                            'postprojectform':postprojectform,
                            'SESSION':request.session,
                            'USER':user
        })
    elif request.method=='POST':
        postprojectform  = ProjectPostingForm(data=request.POST)
        if postprojectform.is_valid():
            err, flag,project_id = saveformtoProject(SESSION=request.session, form=postprojectform)
            messages=[]
            errors=[err]
            if flag:
                messages=[err]
                return projectdetails(request, pid=project_id, message=messages)
                # return render(request, 'stud_dashboard/stud_dashboard.html', {
                #             'SESSION':request.session,
                #             'messages':messages,
                #             'USER':user
                #     })

            else:
                return render(request, 'stud_dashboard/new_project.html', {
                            'postprojectform':postprojectform,
                            'SESSION':request.session,
                            'errors':errors,
                            'USER':user
                    })
        else:

            return render(request, 'stud_dashboard/new_project.html', {
                                            'postprojectform':postprojectform,
                                            'SESSION':request.session,
                                            'USER':user
                })

    else:
        return Http404("Bad Request")


@login_required
@user_passes_test(user_is_student, login_url='/permission_denied')
def listproject(request):
    user = User.objects.get(id=request.session['user_id'])
    errors ,projects = getProjectsForStudent(user_id=user.id)
    return render(request, 'stud_dashboard/all_project.html', {
                    'errors':errors,
                    'projects':projects,
                     'SESSION':request.session,
                     'USER':user
    })


@login_required
@user_passes_test(user_is_student, login_url='/permission_denied')
def projectdetails(request, pid, message=[], errors=[]):
    user=User.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        m,errors=performActionOnProject(project_id=pid, user_id=user.id, action=request.POST.get('action'))
        message = message + (m if m else [])
    e, project, bids=getProjectDetailsForStudent(project_id=pid)
    errors = errors+(e if e else [])
    return render(request, 'stud_dashboard/project_details.html', {
        'errors':errors,
        'project':project,
        'messages':message,
        'bids':bids,
         'SESSION':request.session,
         'USER':user
    })

@login_required
@user_passes_test(user_is_student, login_url='/permission_denied')
def editproject(request, pid):
    user = User.objects.get(id=request.session['user_id'])
    errors,p = getEditableProject(user_id=request.session['user_id'], project_id=pid)
    if errors:
        return projectdetails(request=request, pid=pid , errors=errors)
    else:
        if request.method=='GET':
            postprojectform  = ProjectPostingForm(data={'title':p.title,'description':p.description, 'amount':p.amount, 'due_on':convertTimeToStr(p.due_on), 'subject':p.subject.id, 'id':p.id})
            return render(request, 'stud_dashboard/new_project.html', {
                            'postprojectform':postprojectform,
                            'SESSION':request.session,
                            'USER':user
                })


@login_required
@user_passes_test(user_is_student, login_url='/permission_denied')
def bid(request, pid=None, b_id=None):
    user=User.objects.get(id=request.session.get('user_id',None))
    error=[]
    try:
        bids = Bid.objects.get(id=b_id, deleted_on=None)
    except Exception, e:
        error.append("The Bid had been either deleted or Not Exist")
    try:
        project = Project.objects.get(id=pid, deleted_on=None)
    except Exception, e:
        error.append("The Project does not exist or had been deleted")

    if error:
        return projectdetails(request, pid=pid, errors=error)

    message=[]
    if request.method=='POST':
        #Confirm the bid
        error,message = confirmBid(user_id=request.session.get('user_id',None), project_id=pid, bid_id=b_id)


    return render(request, 'stud_dashboard/bid.html', {
                    'project':project,
                    'bids':bids,
                    'USER':user,
                    'SESSION':request.session,
                    'errors':error,
                    'messages':message
        })


@login_required
def deleteBid(project_id=None):
        deleteBids(project_id=project_id)


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

@login_required
def permission_denied(request):
    return render(request, 'permission_denied.html', {})

