from django import forms
from deployment_app.models import Staff, Team
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class StaffForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), label='', required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), label='', required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}), label='', required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class StaffAdditionalInfoForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}), label='')

    class Meta:
        model = Staff
        fields = ('phone',)


class TeamForm(forms.ModelForm):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Team Name'}), label='', required=True)

    class Meta:
        model = Team
        fields = ('team_name',)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}), label='', max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),  label='', max_length=128, required=True)


class EditProfileForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in format: '+999999999'.Up to 15 digits allowed.")

    photo = forms.ImageField(label="Profile Photo", required=False)
    first_name = forms.CharField(max_length=128, required=True, label="First Name")
    last_name = forms.CharField(max_length=128, required=True, label="Last Name")
    phone = forms.CharField(validators=[phone_regex], max_length=17, required=False, label="Phone Number")
    email = forms.EmailField(label='Email', max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=128, required=True)

