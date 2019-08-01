from django import forms
from .models import *

class NewMaterialForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(NewMaterialForm, self).__init__(*args, **kwargs)
		self.fields['provider'].empty_label = ''
		self.fields['material'].empty_label = ''
		self.fields['paint'].empty_label = ''
		self.fields['other'].empty_label = ''
		self.fields['description'].widget.attrs['placeholder'] = 'Примітка'

	class Meta:
		model = MaterialOrder
		exclude = ['created', 'updated', 'created_by', 'updated_by']

class NewProviderForm(forms.ModelForm):
    
	class Meta:
		model = Provider
		exclude = []

class NewMaterialInForm(forms.ModelForm):
    
	class Meta:
		model = MaterialIn
		exclude = []

class NewPaintInForm(forms.ModelForm):
    
	class Meta:
		model = PaintIn
		exclude = []

class NewOtherInForm(forms.ModelForm):
    
	class Meta:
		model = OtherIn
		exclude = []

class PaidStatusForm(forms.ModelForm):
	class Meta:
		model = MaterialOrder
		fields = ['paid', 'description']