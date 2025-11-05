from django import forms
from .models import Lead


class LeadRegistrationForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone_number', 'age']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition duration-300',
                'placeholder': 'To\'liq ismingizni kiriting'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition duration-300',
                'placeholder': '+998901234567'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition duration-300',
                'placeholder': 'Yoshingiz',
                'min': 1,
                'max': 100
            }),
        }
        labels = {
            'full_name': 'To\'liq ism',
            'phone_number': 'Telefon raqami',
            'age': 'Yosh',
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_number = phone_number.strip()
            if len(phone_number) < 9:
                raise forms.ValidationError('Telefon raqami to\'g\'ri formatda emas')
        return phone_number
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 1 or age > 100):
            raise forms.ValidationError('Yosh 1 va 100 orasida bo\'lishi kerak')
        return age
