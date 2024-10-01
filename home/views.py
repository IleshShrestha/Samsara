from django.shortcuts import render, redirect
from .forms import ContactForm
from .utils import send_email, send_email_attachment



def main(request):
    
    return render(request, 'main.html', {})

def about(request):
    return render(request, 'about.html', {})

def community(request):
    return render(request, 'community.html', {})

def stores(request):

    return render(request, 'stores.html', {})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['first_name']
            message = form.cleaned_data['message']
            image = form['image']
            print(type(image))
            print(image)
            if image is not None:
                send_email_attachment(name, message, image)
                print("sent email with attachment")
            else:
                send_email(name, message)
                print("sent email without attachment")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


