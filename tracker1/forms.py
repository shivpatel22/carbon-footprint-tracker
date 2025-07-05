
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ActivityLog
from .models import UploadRecord

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadRecord
        fields = ['title', 'upload']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['activity_type', 'description', 'input_value']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'input_value': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
