from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm, CommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import CardText, Comment
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'index.html', {'active_tab': 'index'})


def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted")
            return redirect('about')
    else:
        form = ContactForm()
    return render(request, 'about.html', {'active_tab': 'about', 'form': form})


def cities(request):
    card_texts = CardText.objects.all().order_by('id')
    for card in card_texts:
        card.display_content = card.content or 'Content coming soon.'

    paginator = Paginator(card_texts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cities.html',
                  {'active_tab': 'cities',
                   'page_obj': page_obj})


def city_details(request, pk):
    card = get_object_or_404(CardText, id=pk)
    content = card.content if card.content else "Content coming soon"

    # --- Comments -----
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.card = card
        comment.save()
        return redirect('city-details', pk=card.pk)
    else:
        form = CommentForm()

    comments = card.comments.all().order_by('created_at')
    return render(request,
                  'city-details.html',
                  {'active_tab': 'city-details',
                   'card': card, 'content': content,
                   'comments': comments,
                   'form': form, })


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

    return render(request, 'login.html', {'active_tab': 'login', 'form': form})


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('city-details', pk=comment.card.pk)

    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('city-details', pk=comment.card.pk)

    return render(request,
                  'edit-comment.html',
                  {'form': form, 'comment': comment,
                   'active_tab': 'edit-comment'})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('city-details', pk=comment.card.pk)

    if request.method == 'POST':
        card_pk = comment.card.pk
        comment.delete()
        return redirect('city-details', pk=card_pk)

    return render(request,
                  'delete-comment.html',
                  {'comment': comment, 'active_tab': 'delete-comment'})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'logout.html', {'active_tab': 'logout'})


def confirm_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request,
                  'confirm-logout.html', {'active_tab': 'confirm-logout'})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(
            request, f"Account created for {user.username}! You can log in.")
        return redirect('login')

    return render(request,
                  'register.html', {'active_tab': 'register', 'form': form})
