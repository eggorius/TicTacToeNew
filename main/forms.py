import django.forms as forms
from .models import Game


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'aria-describedby': 'basic-addon1'
            })
        }

    def clean(self):
        name = self.cleaned_data['name']
        if Game.objects.filter(name=name).exists():
            raise forms.ValidationError('Game with that name already exists!')
        return self.cleaned_data

