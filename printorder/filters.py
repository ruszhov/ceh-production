from django.contrib.auth.models import User
from .models import *
import django_filters
from django_filters import DateFromToRangeFilter, ChoiceFilter
from django_filters.widgets import RangeWidget
from django import forms

class PrintOrderFilter(django_filters.FilterSet):
	
	# name_of_camp = django_filters.ModelChoiceFilter()	
	image_url = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Частина посилання на файл'}))
	created = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'РРРР-ММ-ДД'}))
	updated_by = django_filters.ModelChoiceFilter(queryset = User.objects.filter(groups__name__in=['Друкарі']))

	def __init__(self, *args, **kwargs):
		super(PrintOrderFilter, self).__init__(*args, **kwargs)
		self.filters['name_of_camp'].field.empty_label = 'Сюжет'
		self.filters['material'].field.empty_label = 'Матеріал'
		self.filters['manager'].field.empty_label = 'Менеджер'
		self.filters['status'].field.empty_label = 'Статус'
		# self.filters['updated_by'].field.queryset = User.objects.filter(groups__name__in=['Друкарі'])
		self.filters['updated_by'].field.empty_label = 'Виконав'

		# for name, field in self.filters.items():
			# if isinstance(field, ChoiceFilter):
			# Add "Any" entry to choice fields.
				# field.extra['name'] = tuple([("", "Any"), ] + list(field.extra['name']))

	class Meta:
		model = PrintOrder
		fields = ['name_of_camp', 'image_url', 'material', 'manager', 'status', 'created', 'updated_by']