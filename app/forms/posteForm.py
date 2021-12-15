from django import forms
from models import Poste


class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ("meteor", "owner", "email", "phone")
