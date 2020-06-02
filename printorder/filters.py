from django.contrib.auth.models import User
from .models import *
import django_filters
from django_filters import DateFromToRangeFilter, ChoiceFilter, BooleanFilter
from django_filters.widgets import RangeWidget, BooleanWidget
from django import forms

from django.shortcuts import render, get_object_or_404, redirect

class PrintOrderFilter(django_filters.FilterSet):

	# name_of_camp = django_filters.ModelChoiceFilter()	
	image_url = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Частина посилання на файл'}))
	created = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'РРРР-ММ-ДД'}))
	updated_by = django_filters.ModelChoiceFilter(queryset = User.objects.filter(groups__name__in=['Друкарі']))
	clean_status = django_filters.BooleanFilter(widget=forms.CheckboxInput, field_name='status', method='filter_clean_status')

	def filter_clean_status(self, queryset, name, value):
		if value is True:
			# lookup = '__'.join([name, 'isnull'])
			# return queryset.filter(**{lookup: True})
			id_of_done = get_object_or_404(PrintStatus, status='Виконано').id
			return queryset.exclude(status = id_of_done)
		else:
			return queryset

	def __init__(self, *args, **kwargs):
		super(PrintOrderFilter, self).__init__(*args, **kwargs)
		self.filters['name_of_camp'].field.empty_label = 'Сюжет'
		self.filters['material'].field.empty_label = 'Матеріал'
		self.filters['print_width'].field.empty_label = 'Ширина'
		self.filters['print_height'].field.empty_label = 'Довжина'
		self.filters['manager'].field.empty_label = 'Менеджер'
		self.filters['status'].field.empty_label = 'Статус'
		self.filters['updated_by'].field.empty_label = 'Виконав'

	class Meta:
		model = PrintOrder
		fields = ['name_of_camp', 'image_url', 'material', 'print_width', 'print_height', 'manager', 'status', 'created', 'updated_by', 'clean_status']