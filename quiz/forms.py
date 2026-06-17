import re

from django import forms

from .models import Lead, QuizResult
from .utils import normalize_phone_number


class LeadRegistrationForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'class': 'hidden',
            'aria-hidden': 'true',
        }),
        label='',
    )

    class Meta:
        model = Lead
        fields = ['full_name', 'phone_number', 'age']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition duration-300',
                'placeholder': 'To\'liq ismingizni kiriting',
                'maxlength': '100',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition duration-300',
                'placeholder': '+998901234567',
                'maxlength': '20',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition duration-300',
                'placeholder': 'Yoshingiz',
                'min': 1,
                'max': 100,
            }),
        }
        labels = {
            'full_name': 'To\'liq ism',
            'phone_number': 'Telefon raqami',
            'age': 'Yosh',
        }

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('So\'rov rad etildi.')
        return ''

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not full_name or len(full_name) < 2:
            raise forms.ValidationError('Ism kamida 2 ta belgidan iborat bo\'lishi kerak.')
        if not re.match(r'^[\w\s\-\.\']+$', full_name, re.UNICODE):
            raise forms.ValidationError('Ismda faqat harflar va bo\'sh joy bo\'lishi mumkin.')
        return full_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Telefon raqami kiritilishi shart.')
        phone_number = normalize_phone_number(phone_number)
        digits = re.sub(r'\D', '', phone_number)
        if len(digits) < 9 or len(digits) > 15:
            raise forms.ValidationError('Telefon raqami to\'g\'ri formatda emas.')
        return phone_number

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 1 or age > 100):
            raise forms.ValidationError('Yosh 1 va 100 orasida bo\'lishi kerak')
        return age

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            return cleaned_data

        existing_lead = Lead.objects.filter(phone_number=phone_number).first()
        if existing_lead and QuizResult.objects.filter(lead=existing_lead).exists():
            raise forms.ValidationError(
                'Bu telefon raqami bilan allaqachon test topshirilgan. '
                'Qayta ishlash mumkin emas.'
            )
        return cleaned_data
