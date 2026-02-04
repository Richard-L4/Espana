from django.shortcuts import render, redirect
from .forms import ContactForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate


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


# ==============================
# User Authentication
# ==============================
def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'])
        if user:
            login(request, user)
            messages.success(request, f"You are logged in as {user.username}")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'logout.html')


def confirm_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'confirm-logout.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(
            request, f"Account created for {user.username}! You can log in.")
        return redirect('login')

    return render(request, 'register.html', {'form': form})
