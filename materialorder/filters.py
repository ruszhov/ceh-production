from django.contrib.auth.models import User
from .models import *
import django_filters
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from django import forms

class MaterialOrderFilter(django_filters.FilterSet):
	invoice = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': '№ рахунку'}))
	# provider__name_of_provider = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Постачальник'}))
	# material__name_of_material = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Матеріал'}))
	# paint__name_of_paint = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Фарба'}))
	# other__name_of_other = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Інше'}))
	# paid = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Інше'}))
	# created = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'ДД/MM/РРРР'}))
	created = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'РРРР-ММ-ДД'}))

	def __init__(self, *args, **kwargs):
		super(MaterialOrderFilter, self).__init__(*args, **kwargs)
		self.filters['provider'].field.empty_label = 'Постачальник'
		self.filters['material'].field.empty_label = 'Матеріал'
		self.filters['paint'].field.empty_label = 'Фарба'
		self.filters['other'].field.empty_label = 'Інше'
		self.filters['paid'].field.empty_label = 'Статус'

	class Meta:
		model = MaterialOrder
		fields = ['invoice', 'provider', 'material', 'paint', 'other', 'paid', 'created']
