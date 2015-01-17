from hw.models import USER_PROFILE

__author__ = 'amd'

from django import forms

class LoginForm(forms.Form):
    fname = forms.CharField(max_length=255, required=True, label='First Name')
    lname = forms.CharField(max_length=255, required=False, label='Last Name')
    email = forms.EmailField(required=True, label='email address')
    confirmemail = forms.EmailField(required=True, label='Confirm email address')
    password = forms.CharField(widget=forms.PasswordInput(),required=True, label='Password')
    confirmpassword = forms.CharField(widget=forms.PasswordInput(),required=True, label='Confirm Password')
    profile = forms.ChoiceField(choices=[(x, y) for x, y in USER_PROFILE], required=True)

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