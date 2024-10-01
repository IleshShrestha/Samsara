from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event
from .forms import EventForm


def all_events(request):
        events = Event.objects.all()
        return render(request, 'all_events.html', {'events': events})

def event(request, pk):
        event = Event.objects.get(id=pk)
        return render(request, 'event.html', {'events': event})



