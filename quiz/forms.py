from django import forms
from .models import Student


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'phone_number', 'age']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'To\'liq ismingizni kiriting'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+998901234567'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-input',
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
            # Basic validation - can be enhanced
            phone_number = phone_number.strip()
            if len(phone_number) < 9:
                raise forms.ValidationError('Telefon raqami to\'g\'ri formatda emas')
        return phone_number
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 1 or age > 100):
            raise forms.ValidationError('Yosh 1 va 100 orasida bo\'lishi kerak')
        return age

