from django import forms

from core.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['excel']


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
