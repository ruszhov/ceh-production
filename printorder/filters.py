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
		self.filters['print_width'].field.empty_label = 'Ширина'
		self.filters['print_height'].field.empty_label = 'Довжина'
		self.filters['manager'].field.empty_label = 'Менеджер'
		self.filters['status'].field.empty_label = 'Статус'
		# self.filters['updated_by'].field.queryset = User.objects.filter(groups__name__in=['Друкарі'])
		self.filters['updated_by'].field.empty_label = 'Виконав'

		# for name, field in self.filters.items():
			# if isinstance(field, ChoiceFilter):
			# Add "Any" entry to choice fields.
				# field.extra['name'] = tuple([("", "Any"), ] + list(field.extra['name']))

		# def get_current_path(request):
		#     return {
		#     	# 'current_path': request.get_full_path()
		#     	'current_path': request.build_absolute_url()
		#     }
		#     request.session['current_path'] = current_path
		#     # print(request.session['current_path'])

	class Meta:
		model = PrintOrder
		fields = ['name_of_camp', 'image_url', 'material', 'print_width', 'print_height', 'manager', 'status', 'created', 'updated_by']