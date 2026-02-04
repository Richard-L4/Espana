from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone',
            'message': 'Message',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter your full name'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Please enter your email.'}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Please enter your phone number'}
            ),
            'message': forms.Textarea(
                attrs={'placeholder': 'Please enter your message'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False
