from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Count
from hw.models import Subject, Project, Bid
import re

def getAllSubjectsName():
    subjects = Subject.objects.values('id','name').all()
    # subjects = [{'name': u'Computer Science'}, {'name': u'Physics'}, {'name': u'Chemistry'}, {'name': u'Biology'}, {'name': u'Mathematics'}, {'name': u'English'}]
    return subjects

def validateDateTime(date_time=None,total_seconds=1800):
    #expected DD MM YYYY HH:MM
    def match(str ):
        search = re.compile(r'\d{2} \d{2} \d{4} \d{2}:\d{2}$')
        return bool(search.match(str))

    if not date_time:
        return False
    date_time = date_time.strip()
    day = int(date_time[0:2])
    month = int(date_time[3:5])
    year = int(date_time[6:10])
    hour = int(date_time[11:13])
    min = int(date_time[14:16])

    now = datetime.now()
    due_on = datetime(year, month, day, hour , min)
    total_secs = (due_on - now).total_seconds()
    if total_secs >= total_seconds:
        return due_on, True
    else:
        return "Due time cannot me less than 30 minutes from now", False

def convertTimeToStr(time=None):
    def clean(s,l=2):
        length = len(s)
        return "0"*(l-length)+s

    try:
        yyyy=clean(str(time.year),l=4)
        dd = clean(str(time.day))
        mm = clean(str(time.month))
        hh = clean(str(time.hour))
        min= clean(str(time.minute))
        return dd+" "+mm+" "+yyyy+" "+hh+":"+min
    except Exception, e:
        print e
        convertTimeToStr(time=datetime.now())


def saveformtoProject(SESSION=None, form=None):
    try:
        formdata = form.cleaned_data
        #{'due_on': u'21312312', 'amount': 0.0, 'subject': u'1', 'description': u'', 'title': u'sadasdqwwqdqwdqwdqwd'}
        user = User.objects.get(id=SESSION['user_id'])

        project = Project()
        duetime,flag = validateDateTime(formdata['due_on'])
        if flag:
            project.due_on = duetime
        else:
            return duetime, False , None

        project.user = user



        project.title = formdata['title']
        project.description = formdata['description']
        project.amount = formdata['amount']
        project.subject = Subject.objects.get(id=int(formdata['subject']))
        project.status = 'LIVE'
        # if Project.objects.filter(user=project.user, title=project.title, description=project.description, amount=project.amount, status=project.status, subject=project.subject).__len__()>0:
        #     return "Your Project is already Posted",False
        if formdata['id']:
            Project.objects.filter(id=formdata['id']).update(user=project.user, title=project.title, description=project.description, amount=project.amount, status=project.status, subject=project.subject, due_on=duetime)
            return "You Project has been successfully Modified ",True,formdata['id']
        project.save()
        return "You Project has been successfully Placed ",True, project.id
    except Exception,e:
        print e
        return "Something Went Wrong", False



