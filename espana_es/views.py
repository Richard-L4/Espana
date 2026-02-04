from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted")
            return redirect('about')
    else:
        form = ContactForm()
    return render(request, 'about.html', {'form': form})


def cities(request):
    return render(request, 'cities.html')


def city_details(request):
    return render(request, 'city-details.html')


def confirm_logout(request):
    return render(request, 'confirm-logout.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'logout.html')


def register(request):
    return render(request, 'register.html')
