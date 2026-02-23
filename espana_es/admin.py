from django.contrib import admin
from .models import Contact, CardText, Comment, CommentReaction


# Register your models here.

# -------------
# Contact
# -------------
@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('name', 'email')


# --------------
# Card Text
# ---------------

@admin.register(CardText)
class CardTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_content', 'image_name')

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
