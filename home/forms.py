from django import forms
from django.core.validators import EmailValidator
from .models import contact

class ContactForm(forms.Form):

    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    phone = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    subject = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'subject'}))
    message = forms.CharField(label="", max_length=300, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Message'}))
    image = forms.ImageField(required=False)


    class Meta:
        model = contact
        fields = ('email', 'first_name', 'last_name', 'phone', 'subject', 'message', 'image')