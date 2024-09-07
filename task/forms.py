
from django import forms
from django.contrib.auth.models import User
from task.models import Categorie, Task

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class SiginForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=3, required=True)
    password = forms.CharField(max_length=50, min_length=3, required=True)


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ('name', )
        widjets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('categorie', 'title', 'description', 'start_date', 'end_date', 'priority')
        widgets = {
            'categorie': forms.Select(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
            'start_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary','type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary','type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].empty_label = "Cliquez pour choisir"
        