from django import forms

class LogForm(forms.Form):
    date_from = forms.CharField(max_length=30)
    date_to = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(LogForm, self).clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')