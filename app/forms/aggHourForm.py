from django.forms import forms
from models import AggHour


class AggHourForm(forms.ModelForm):
    class Meta:
        model = AggHour
        fields = ("poste", "j")
