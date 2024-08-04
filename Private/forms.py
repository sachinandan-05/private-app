from django import forms

from .models import PrivateModel


class PrivateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['private_description'].required = False
        self.fields['date_name'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
            }
        )
        self.fields['title'].widget = forms.widgets.TextInput(
            attrs={
                'placeholder': 'Title',
                'class': 'form-control'
            }
        )

    class Meta:
        model = PrivateModel
        exclude = ['user']
        fields = ['date_name', 'private_description', 'title', 'share']
