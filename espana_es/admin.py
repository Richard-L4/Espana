from django.contrib import admin
from .models import Contact, CardText

# Register your models here.

# -------------
# Contact
# -------------
admin.site.register(Contact)


# --------------
# Card Text
# ---------------

@admin.register(CardText)
class CardTextAdmin(admin.ModelAdmin):
    list_display = ('title',)
