

from django import template
from django.conf import settings
from hw.models import Project, PROJECT_STATUS, Bid, BID_CHOICES

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

