from django import forms
from django.forms import ModelForm
from .models import Event

class EventFormInfo(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'location', 'description')

class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'event_date':DateInput(format=["%Y-%m-%d"],),
            'event_description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),

        }
