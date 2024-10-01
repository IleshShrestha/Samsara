from django.shortcuts import render
from django.http import HttpResponseRedirect


def blog(request):
    
    return render(request, 'main.html', {})

