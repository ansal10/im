from hw.homework.helper import getAllSubjectsName, validateDateTime
from hw.models import USER_PROFILE, Project

__author__ = 'amd'

from django import forms

class RegisterForm(forms.Form):
    fname = forms.CharField(max_length=255, required=True, label='First Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}))
    lname = forms.CharField(max_length=255, required=True, label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}))
    email = forms.EmailField(required=True, label='email address', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email address'}))
    confirmemail = forms.EmailField(required=True, label='Confirm email address', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Confirm email address'}))
    username = forms.CharField(max_length=255, required=True, label='Username', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),required=True, label='Password')
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm Password'}),required=True, label='Confirm Password')
    profile = forms.ChoiceField(choices=[(x, y) for x, y in USER_PROFILE], required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_email(self):
        if self.data['email'] != self.data['confirmemail']:
            raise forms.ValidationError('Emails are not the same')
        return self.data['email']

    def clean_password(self):
        if self.data['password'] != self.data['confirmpassword']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self,*args, **kwargs):
        self.clean_email()
        self.clean_password()
        return super(RegisterForm, self).clean(*args, **kwargs)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True,  widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),required=True, label='Password')
    profile = forms.ChoiceField(choices=[(x, y) for x, y in USER_PROFILE], required=True, widget=forms.Select(attrs={'class': 'form-control'}))


class ProjectPostingForm(forms.Form):

    title = forms.CharField(max_length=512, required=True, min_length=20, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Brief about your Project'}))
    description = forms.CharField(max_length=25500, widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Description about your project (NOT MANDATORY)'}), required=False)
    amount = forms.FloatField(min_value=0.0, required=True ,widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Your Budget ( you can even declare 0 )'}), )
    subject = forms.ChoiceField(choices=[(x['id'],x['name']) for x in getAllSubjectsName()], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    due_on = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'DD MM YYYY HH:MM (24 hours format)'}), required=True)
    id = forms.IntegerField(widget=forms.HiddenInput(),label="", required=False)

    def clean_datetime(self):
        date_time = self.data['due_on']
        try:
            errors, flag =validateDateTime(date_time)
            if flag:
                return self.data['due_on']
            else:
                self._errors['due_on'].append(errors)
                raise forms.ValidationError(errors)
        except Exception, e:
            raise forms.ValidationError('Date time does not match Expected Format')

    def clean(self, *args, **kwargs):
        self.clean_datetime()
        return super(ProjectPostingForm, self).clean(*args, **kwargs)

class BidForm(forms.Form):
    amount = forms.FloatField(min_value=0.0, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Place your bid Amount'}), required=True)
    deliver_by =forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'DD MM YYYY HH:MM (24 hours format)'}), required=True)
    description = forms.CharField(max_length=25500, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'How you think you are good for this project (NOT MANDATORY)'}), required=False)
    deletable = forms.BooleanField(widget=forms.HiddenInput(), label="", required=False)

    def clean_datetime(self):
        date_time = self.data['deliver_by']
        try:
            errors, flag =validateDateTime(date_time,total_seconds=180)
            if flag:
                return self.data['deliver_by']
            else:
                self._errors['deliver_by'].append(errors)
                raise forms.ValidationError(errors)
        except Exception, e:
            print e
            raise forms.ValidationError('Date time does not match Expected Format')

    def clean(self, *args, **kwargs):
        self.clean_datetime()
        return super(BidForm, self).clean(*args, **kwargs)
