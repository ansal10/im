from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from hw.models import Project, Bid


def getProjectDetailsForStudent(project_id=None):
    try:
        project = Project.objects.get(id=project_id)

        bids={}

        for b in Bid.objects.filter(project_id=project_id, deleted_on=None):
            bids.update({b:User.objects.values('id','username').get(id=b.user_id)})

        return [], project,bids
    except Exception, e:
        return ["No Project Exist By this ID"], None,None


def getProjectDetailsForScholar(project_id=None):
    try:
        project = Project.objects.get(id=project_id)
        if project.assigned_to:
            return ["The project You requested had already been Assigned to someone Else"],None,None

        bids={}
        for b in Bid.objects.filter(project_id=project_id, deleted_on=None):
            bids.update({b:User.objects.values('id','username').get(id=b.user_id)})

        return [], project,bids
    except Exception, e:
        return ["No Project Exist By this ID"], None,None



ACTIONS=['delete','makelive']
def performActionOnProject(project_id=None, user_id=None , action=None):
    if not action:
        return [],[]
    if not project_id:
        return [],["Project ID not Passed"]
    p = Project.objects.filter(id=project_id , user_id=user_id)
    if p.__len__()==0:
        return ["This Project Does Not belong to you"],None
    if action not in ACTIONS:
        return ["The Action "+action+" is not defined"],None
    p=p[0]
    if action==ACTIONS[0]:
        p.deleted_on=datetime.now()
        p.status='EXPR'
        p.save()
        return ["Successfully Removed From Bidding List"],None
    elif action==ACTIONS[1]:
        p.deleted_on=None
        p.status='LIVE'
        p.save()
        return ["Project is Successfully Added to Bidding List"],None


def getEditableProject(user_id=None, project_id=None):

    try:
        p = Project.objects.filter(user_id=user_id , id=project_id)[0]
        if p.deleted_on is not None:
            return ["The project is Expired Or Deleted by You , Please make it live first"], None
        else:
            return [],p

    except Exception, e:
        print e
        return ["Some Error Occured , it seems Project does not exist! "], None

def getProjectsForStudent(user_id=None):
    try:
        p1 = Project.objects.filter(user_id=user_id).order_by('-created_on')
        return None,p1
    except Exception, e:
        print e
        return ["Error Retrieving Project or no such user exist"],None

def getProjectsForScholar(subject=None, project_id=None):
    q = Q(deleted_on=None)
    if subject:
        q = q&Q(subject__name__iexact=subject)
    if project_id:
        q = q&Q(id=project_id)
    projects = Project.objects.filter(q).order_by('-id')
    print projects.__len__()
    return projects


