from django import forms
from django.forms import Field
from django.utils.translation import ugettext_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		labels = {
			'username': 'Votre Nom',
			'email': '  Adresse email ',
			'password1': ' Mots de passe ',
			'password2': ' Confirmer votre mots de passe ',
		}


	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user