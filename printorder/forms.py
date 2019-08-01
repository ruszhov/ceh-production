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
		# self.fields['tmp_number'].required = False
		# self.fields['tmp_updated_by'].required = False

	class Meta:
		model = PrintOrder
		fields = ['description']

class NewCampaignForm(forms.ModelForm):
    
	class Meta:
		model = CampaignName
		exclude = []


class EditDoneStepsForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(EditDoneStepsForm, self).__init__(*args, **kwargs)

		self.fields['tmp_number'].required = False
		self.fields['print_order'].required = False
		self.fields['created_by'].required = False
		self.fields['updated_by'].required = False

	class Meta:
		model = DoneSteps
		fields = ('tmp_number', 'print_order', 'created_by', 'updated_by')
