import datetime
import pdb
from django import template
from django.conf import settings
from hw.models import Project, PROJECT_STATUS, Bid, BID_CHOICES
import pytz

register = template.Library()

@register.filter(name='stud_projects_count')
def stud_projects_count(value):
    len = Project.objects.filter(user_id=value).__len__()
    return str(len)

@register.filter
def get_mapping_from_project_status(value):
    for x,y in PROJECT_STATUS:
        if x==value:
            return y
    return None

@register.filter
def total_bids(value):
    return Bid.objects.values('id').filter(user=value).__len__()

@register.filter
def get_mapping_from_bids_status(value):
    for x,y in BID_CHOICES:
        if x==value:
            return y
    return None

@register.filter
def get_bids_for_project(value):
    return Bid.objects.filter(project=value, deleted_on=None)

@register.filter
def time_left_from_now(value):
    now= datetime.datetime.now(pytz.UTC)
    if now>value:
        return "Your Time is elasped , Huryy if u have not Completed till Now . Student Can any time file a Complain against you and you will loose the money"
    timeleft = value-now
    messege=""
    messege += "%s Days, "%(timeleft.days) if timeleft.days else "0"
    messege += "%s Hours and "%(timeleft.seconds/3600) if timeleft.seconds/3600 else "0"
    messege += "%s Minutes. "%((timeleft.seconds%3600)/60) if (timeleft.seconds%3600)/60 else "0"

    return messege
