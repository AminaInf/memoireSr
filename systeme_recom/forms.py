from django.forms import ModelForm
from django import forms
from .models import Culture

class CultureForm(ModelForm):
    typeCultu= [
        ('Pluviale', 'Pluviale'),
        ('irrigue', 'irrigue'),
    ]
    sols = [
        ('Argileux ', 'Argileux '),
        ('sableux', 'sableux'),
        ('deck', 'deck'),
    ]
    sol = forms.TypedChoiceField(required=False,widget=forms.Select, choices=sols)
    typeCulture = forms.TypedChoiceField(choices=typeCultu, widget=forms.RadioSelect)
    class Meta:
        model = Culture
        fields = ['temperature', 'ph','typeCulture','sol']
        widgets = {
            'temperature': forms.TextInput(),
            'ph': forms.NumberInput(),
            'typeCulture': forms.RadioSelect(),
            'sol': forms.Select(),
        }  # override the type that overrides the title field
        labels = {
            'temperature': ' Temperature en °C ',
            'ph': ' Potentiel Hydrogene ',
            'typeCulture': ' Type de Culture ',
            'sol': ' Tyepe de sol ',

        }

        # def __init__(self, *args, **kwargs):
        #     self.request = kwargs.pop('request', None)
        #     return super(CultureForm, self).__init__(*args, **kwargs)
        #
        # def save(self, *args, **kwargs):
        #     kwargs['commit'] = False
        #     obj = super(CultureForm, self).save(*args, **kwargs)
        #     if self.request:
        #         obj.user = self.request.user
        #     obj.save()
        #     return obj
        # # error_messages = {
        # #     'name': {
        # #         'max_length': ' the name is less than 15 characters long ',
        # #     }
        # # }




