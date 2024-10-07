from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Document,BloodCount

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_name', 'document_file']



class BloodCountForm(forms.ModelForm):
    class Meta:
        model = BloodCount
        fields = ['file']
