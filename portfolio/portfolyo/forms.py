from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'custom-input',
                'placeholder': 'Adınız Soyadınız',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'custom-input',
                'placeholder': 'E-posta Adresiniz',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'custom-input',
                'placeholder': 'Konu',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'custom-input',
                'placeholder': 'Mesajınız',
                'rows': 5,
                'required': True
            }),
        }
