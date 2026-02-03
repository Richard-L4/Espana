from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


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
