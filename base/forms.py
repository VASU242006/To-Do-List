# from To_Do_List.base.models import TODO
from django.contrib.auth import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, widgets, ModelForm
from django import forms
from django.forms.forms import Form
from base.models import TODO
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import DateInput


class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpform(UserCreationForm):
  
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.widgets.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {'email': 'Email'}


class LoginUpform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class TODOForm(ModelForm):

    end_date = forms.DateField(widget=DateInput)
    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority', 'end_date']
        
        


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # fields=['username','email']
        fields = ['username', 'email']


class viewTodoForm(TODOForm):

    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority', 'end_date']


class changePassForm(forms.ModelForm):

    currentPassword = forms.CharField(
        label='Current Password', widget=forms.widgets.PasswordInput)

    newPassword = forms.CharField(
        label='New Password', widget=forms.widgets.PasswordInput)

    confirmPassword = forms.CharField(
        label='Confirm Password', widget=forms.widgets.PasswordInput)

    class Meta:
        model = User
        fields = ['currentPassword', 'newPassword', 'confirmPassword']
