from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm, CommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import CardText, Comment, CommentReaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction


# Create your views here.
def index(request):
    lang = request.GET.get('lang', 'en')
    spain_intro = {
        'en': [
            (
                "Spain, stretching across the Iberian Peninsula"
                " between the Atlantic and Mediterranean,"
                " weaves centuries of history, passionate culture,"
                " and breathtaking landscapes"
                " into a single unforgettable nation."
            ),
            (
                "Its storied cities pulse with life —"
                " Madrid's grand boulevards and world-class museums,"
                " Barcelona's Gaudí masterpieces and Gothic Quarter,"
                " Seville's flamenco rhythms and Moorish palaces."
                " Every street corner holds a story."
            ),
            (
                "From the snow-capped Pyrenees"
                " to sun-drenched Andalusian plains,"
                " Spain's landscapes are as varied as its regions."
                " Visitors feast on tapas, sip Rioja,"
                " and linger over long lunches"
                " as the Mediterranean sun dips toward the horizon."
            ),
            (
                "Festivals ignite every calendar —"
                " the Running of the Bulls in Pamplona,"
                " La Tomatina in Buñol,"
                " Semana Santa processions that stop time."
                " Here, tradition is not preserved behind glass;"
                " it lives, dances, and roars."
            ),
            (
                "With warmth in its people, fire in its soul,"
                " and beauty around every bend,"
                " Spain offers a Mediterranean spirit like no other"
                " — one that stays with you"
                " long after you've left its shores."
            ),
        ],
        'es': [
            (
                "España, extendida por la Península Ibérica"
                " entre el Atlántico y el Mediterráneo,"
                " entrelaza siglos de historia,"
                " cultura apasionada y paisajes impresionantes"
                " en una nación única e inolvidable."
            ),
            (
                "Sus legendarias ciudades vibran con vida —"
                " los grandes bulevares y museos de Madrid,"
                " las obras maestras de Gaudí"
                " y el Barrio Gótico de Barcelona,"
                " los ritmos del flamenco"
                " y los palacios árabes de Sevilla."
                " En cada rincón hay una historia que contar."
            ),
            (
                "Desde los nevados Pirineos"
                " hasta las soleadas llanuras andaluzas,"
                " los paisajes de España son tan variados"
                " como sus regiones."
                " Los visitantes disfrutan de tapas,"
                " saborean un Rioja y se deleitan"
                " con largas sobremesas mientras el sol"
                " mediterráneo se hunde en el horizonte."
            ),
            (
                "Los festivales encienden cada rincón del calendario"
                " — los Sanfermines en Pamplona,"
                " la Tomatina en Buñol,"
                " las procesiones de Semana Santa"
                " que detienen el tiempo."
                " Aquí, la tradición no se conserva tras un cristal;"
                " vive, baila y ruge."
            ),
            (
                "Con calidez en su gente,"
                " fuego en su alma y belleza a cada paso,"
                " España ofrece un espíritu mediterráneo"
                " como ningún otro — uno que permanece contigo"
                " mucho después de haber dejado sus costas."
            ),
        ],
    }
    content_paragraphs = spain_intro.get(lang, spain_intro['en'])
    return render(request, 'index.html', {
        'active_tab': 'index',
        'content_paragraphs': content_paragraphs,
        'lang': lang,
    })


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
    lang = request.GET.get('lang', 'en')
    card_texts = CardText.objects.all().order_by('id')
    for card in card_texts:
        translation = card.translations.filter(language=lang).first()
        card.translated_content = (
            translation.content
            if translation else card.content or 'Content coming soon.'
        )

    paginator = Paginator(card_texts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cities.html',
                  {'active_tab': 'cities',
                   'page_obj': page_obj,
                   'lang': lang})


def city_details(request, pk):
    card = get_object_or_404(CardText, id=pk)
    # 🌍 Language system (unchanged)
    lang = request.GET.get('lang', 'en')
    translation = card.translations.filter(language=lang).first()
    content = (
        translation.content
        if translation
        else card.content or 'Content coming soon.'
    )

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
                   'card': card,
                   'content': content,
                   'comments': comments,
                   'form': form,
                   'lang': lang,
                   })


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


# ==============================
# Comment Reactions (Like/Dislike)
# ==============================

@login_required
def toggle_reaction(request, comment_id, reaction_type):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    comment = get_object_or_404(Comment, id=comment_id)
    with transaction.atomic():
        existing = CommentReaction.objects.filter(user=request.user,
                                                  comment=comment).first()
        if existing:
            if existing.reaction != reaction_type:
                existing.reaction = reaction_type
                existing.save()
                status = 'changed'
            else:
                status = 'unchanged'
        else:
            CommentReaction.objects.create(user=request.user, comment=comment,
                                           reaction=reaction_type)
            status = 'added'

        likes_count = comment.reactions.filter(reaction='like').count()
        dislikes_count = comment.reactions.filter(reaction='dislike').count()

    return JsonResponse({'status': status, 'likes': likes_count,
                        'dislikes': dislikes_count})
