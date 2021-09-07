from django import forms
from .models import FileForAnalysis


class DocumentForm(forms.ModelForm):
    class Meta:
        model = FileForAnalysis
        fields = ('upload', )
        widgets = {'upload': forms.FileInput(attrs={'class': 'form-control'})}
        labels = {'upload': '', }
