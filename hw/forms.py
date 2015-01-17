from hw.models import USER_PROFILE

__author__ = 'amd'

from django import forms

class RegisterForm(forms.Form):
    fname = forms.CharField(max_length=255, required=True, label='First Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}))
    lname = forms.CharField(max_length=255, required=False, label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}))
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
        return super(LoginForm, self).clean(*args, **kwargs)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True,  widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),required=True, label='Password')
    profile = forms.ChoiceField(choices=[(x, y) for x, y in USER_PROFILE], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
