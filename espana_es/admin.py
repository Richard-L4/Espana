from django.contrib import admin
from .models import Contact, CardText, Comment, CommentReaction, \
    CardTextTranslation, EventRating
from django.db.models import Avg


# Register your models here.

# -------------
# Contact
# -------------
@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('name', 'email')


# ------------------------
# CardText with translations and ratings
# ------------------------

class CardTextTranslationInline(admin.TabularInline):
    model = CardTextTranslation
    extra = 1


class EventRatingInline(admin.TabularInline):
    model = EventRating
    extra = 0
    readonly_fields = ('user', 'rating')


@admin.register(EventRating)
class EventRatingAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'rating')
    list_filter = ('card', 'rating')
    search_fields = ('card__title', 'user__username')

# --------------
# Card Text
# ---------------


@admin.register(CardText)
class CardTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_content', 'image_name')
    inlines = [CardTextTranslationInline]

    def average_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    average_rating.short_description = 'Avg Rating'

    def rating_count(self, obj):
        return obj.ratings.count()
    rating_count.short_description = 'Number of Ratings'

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"


# ------- Comments -----
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_dislplay = ('comment_preview', 'user', 'created_at')

    def comment_preview(self, obj):
        return obj.text[:50]

    comment_preview.short_description = 'Comment'


# ------------------------
# CommentReaction admin
# ------------------------

class CommentReactionInLine(admin.TabularInline):
    model = CommentReaction
    extra = 0
    readonly_fields = ('user', 'reaction')


@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment', 'reaction')
