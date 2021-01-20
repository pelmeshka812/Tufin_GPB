from django import forms

from core.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['excel']