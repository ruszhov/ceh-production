from django import forms
from .models import *

class NewOrderForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(NewOrderForm, self).__init__(*args, **kwargs)

		self.fields['image_url'].widget.attrs['placeholder'] = 'Вставте сюди посилання на файл'
		# self.fields['name_of_camp'].widget = forms.SelectMultiple(attrs={'size':'40px'})

	class Meta:
		model = PrintOrder
		exclude = ['created', 'updated', 'created_by', 'updated_by']
		# widgets = {
  		#           'name_of_camp': forms.SelectMultiple(attrs={'size': 50})
  		#       }

class EditStatusForm(forms.ModelForm):
	class Meta:
		model = PrintOrder
		fields = ['status', 'description']

class EditDescForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(EditDescForm, self).__init__(*args, **kwargs)

		self.fields['description'].widget.attrs['placeholder'] = 'Примітка'
		# self.fields['description'].widget.attrs['size=40']
		# self.fields['description'].widget = forms.SelectMultiple(attrs={'height':'40px'})

	class Meta:
		model = PrintOrder
		fields = ['description']

class NewCampaignForm(forms.ModelForm):
    
	class Meta:
		model = CampaignName
		exclude = []


