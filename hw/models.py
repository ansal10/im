from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
PROJECT_STATUS = (
    ('LIVE', _('Live')),
    ('PROG', _('In Progress')),
    ('COMP', _('Completed')),
    ('DISP', _('Disputed')),
    ('EXPR', _('Expired')),
)
MESSAGE_STATUS = (
    ('READ', _('Read')),
    ('UNREAD', _('Not Read')),
)
USER_PROFILE = (
    ('SCHOLAR', _('Scholar')),
    ('STUD', _('Student')),
)
STUDENT_CATEGORY = (
    ('NEW' , _('New Student')),
    ('OLD', _('Old Student')),
)
SCHOLAR_CATEGORY = (
    ('FRESHER',_('Fresher')),
    ('EXPERIENCE', _('Experienced')),
    ('EXPERT', _('Expert')),
)
BID_CHOICES = (
    ('ACTIVE', _('Active')),
    ('WINS', _('Winner')),
    ('DEL', _('Deleted')),
    ('PAID', _('Paid')),
    ('UNPAID', _('Unpaid')),
    ('CLOSE', _('Closed')),
    ('DENY',_('Denied'))
)
class File(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('Filename'))
    extension = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('extension'))
    deleted_on=models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Deleted On'), db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    content = models.FileField(upload_to=name)

class Subject(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('Name'))
    deleted_on=models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Deleted On'), db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))

class Project(models.Model):
    user = models.ForeignKey(User, db_index=True, null=False)
    assigned_to = models.ForeignKey(User, null=True, verbose_name=_('Alloted to'), related_name='assigned')
    assigned_on = models.DateTimeField(null=True, verbose_name=_('Alloted on'))

    title = models.CharField( max_length=255, blank=False, verbose_name=_('Title') )
    description = models.TextField( verbose_name=_('Description'))
    amount = models.FloatField(max_length=255, default=0, validators=[MinValueValidator(0.0)], verbose_name=_('Budget'))
    deleted_on = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Deleted On'), db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    last_updated_on = models.DateTimeField(auto_now=True, verbose_name=_('Last Updated On'), blank=True, null=True, default=None)
    due_on = models.DateTimeField(null=False, blank=False, verbose_name=_('Due on'))
    status = models.CharField(max_length=255, null=False, db_index=True, choices=PROJECT_STATUS)
    subject = models.ForeignKey(Subject, blank=False, db_index=True, null=False)

    upload1 = models.ForeignKey(File, null=True, blank=True, verbose_name=_('File 1'), related_name='project_upload1')
    upload2 = models.ForeignKey(File, null=True, blank=True, verbose_name=_('File 2'), related_name='project_upload2')
    upload3 = models.ForeignKey(File, null=True, blank=True, verbose_name=_('File 3'), related_name='project_upload3')

class Solution(models.Model):
    user = models.ForeignKey(User , db_index=True, null=False)
    project = models.ForeignKey(Project, db_index=True, null=False, blank=False)
    description = models.TextField( verbose_name=_('Description'))

    deleted_on=models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Deleted On'), db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    last_updated_on=models.DateTimeField(auto_now=True, verbose_name=_('Last Updated On'), blank=True, null=True, default=None)

    upload1 = models.ForeignKey(File, null=True, blank=True, verbose_name=_('File 1'), related_name='solution_upload1')
    upload2 = models.ForeignKey(File, null=True, blank=True, verbose_name=_('File 2'), related_name='solution_upload2')
    upload3 = models.ForeignKey(File, null=True, blank=True, verbose_name=_('File 3'), related_name='solution_upload3')

class Message(models.Model):
    sender = models.ForeignKey(User , blank=False, null=False, db_index=True, related_name='sender')
    reciever = models.ForeignKey(User, blank=False, null=False, db_index=True, related_name='reciever')
    message = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    status = models.CharField(max_length=255, null=False, db_index=True, choices=MESSAGE_STATUS)

class Profile(models.Model):
    user = models.OneToOneField(User)
    profile = models.CharField(max_length=255, blank=False, null=False, choices=USER_PROFILE)
    balance = models.FloatField(max_length=255, default=0, validators=[MinValueValidator(0.0)],verbose_name=_('Balance'))
    category = models.CharField(max_length=255, choices=STUDENT_CATEGORY+SCHOLAR_CATEGORY, null=False)
    degree = models.CharField(max_length=255, null=False, blank=False)

class Bid(models.Model):
    project = models.ForeignKey(Project, null=False, db_index=True)
    user = models.ForeignKey(User, null=False, db_index=True, blank=False)
    description = models.TextField( verbose_name=_('Description'))
    is_sealed = models.BooleanField(default=False, verbose_name=_('Sealed'))
    status = models.CharField(max_length=255, null=False, choices=BID_CHOICES, db_index=True, verbose_name=_('Status') )
    amount = models.FloatField(max_length=255, default=0, validators=[MinValueValidator(0.0)], verbose_name=_('Amount'))
    deliever_by = models.DateTimeField(null=False, blank=False, verbose_name=_('Deliever By'))

    deleted_on=models.DateTimeField(blank=True, null=True, default=None, verbose_name=_('Deleted On'), db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    last_updated_on=models.DateTimeField(auto_now=True, verbose_name=_('Last Updated On'), blank=True, null=True, default=None)
