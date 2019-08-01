from django.db import models
from django.contrib.auth.models import User

class Provider(models.Model):
	name_of_provider = models.CharField(max_length=50)
	description = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name_of_provider

	class Meta:
		verbose_name = 'Постачальник'
		verbose_name_plural = 'Постачальники'
		ordering = ['name_of_provider']

class MaterialIn(models.Model):
	name_of_material = models.CharField(max_length=50)
	description = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name_of_material

	class Meta:
		verbose_name = 'Матеріал'
		verbose_name_plural = 'Матеріали'
		ordering = ['name_of_material']

class PaintIn(models.Model):
	name_of_paint = models.CharField(max_length=50)
	description = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name_of_paint

	class Meta:
		verbose_name = 'Чорнило'
		verbose_name_plural = 'Чорнила'
		ordering = ['name_of_paint']

class OtherIn(models.Model):
	name_of_other = models.CharField(max_length=50)
	description = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name_of_other

	class Meta:
		verbose_name = 'Інше'
		verbose_name_plural = 'Все інше'
		ordering = ['name_of_other']


class MaterialOrder(models.Model):
	invoice = models.CharField("№ рахунку", max_length=30, blank=False)
	provider = models.ForeignKey(Provider, blank=False, null=True, default=None, on_delete = models.DO_NOTHING,)
	material = models.ForeignKey(MaterialIn, blank=True, null=True, default=None, on_delete = models.DO_NOTHING)
	material_width = models.FloatField("Ширина", blank=True, null=True, default=None)
	material_height = models.FloatField("Довжина", blank=True, null=True, default=None)
	number_of_material = models.IntegerField("Кількість", blank=True, null=True, default=None)
	m_kv_of_material = models.DecimalField("м.кв.", max_digits=9, decimal_places=2, null=True, blank=True)
	total_of_material = models.DecimalField("Сума без ПДВ", max_digits=9, decimal_places=2, null=True, blank=True)
	total_of_material_pdv = models.DecimalField("Сума з ПДВ", max_digits=9, decimal_places=2, null=True, blank=True)
	paint = models.ForeignKey(PaintIn, blank=True, null=True, default=None, on_delete = models.DO_NOTHING,)
	litr_of_paint = models.DecimalField("Літри",max_digits=9, decimal_places=2, null=True, blank=True)
	number_of_litres = models.IntegerField("К-ть літрів", blank=True, null=True, default=None)
	all_litres = models.DecimalField("Всього літрів", max_digits=9, decimal_places=2, null=True, blank=True)
	total_of_paint = models.DecimalField("Сума без ПДВ", max_digits=9, decimal_places=2, null=True, blank=True)
	total_of_paint_pdv = models.DecimalField("Сума з ПДВ", max_digits=9, decimal_places=2, null=True, blank=True)
	other = models.ForeignKey(OtherIn, blank=True, null=True, default=None, on_delete = models.DO_NOTHING,)
	packing_of_other = models.DecimalField("Упаковка", max_digits=9, decimal_places=2, null=True, blank=True)
	number_of_other = models.IntegerField("К-ть", blank=True, null=True, default=None)
	all_of_other = models.DecimalField("Всього", max_digits=9, decimal_places=2, null=True, blank=True)
	total_of_other = models.DecimalField("Сума без ПДВ", max_digits=9, decimal_places=2, null=True, blank=True)
	total_of_other_pdv = models.DecimalField("Сума з ПДВ", max_digits=9, decimal_places=2, null=True, blank=True)
	description = models.TextField("Опис", max_length=100, blank=True, null=True)
	CHOICES = ((None, "Неоплачено"), (True, "Оплачено"))
	paid = models.NullBooleanField(choices = CHOICES)
	created_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='created', default=None, null=True)
	updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='updated', default=None, null=True)
	created = models.DateTimeField("Запис створено", auto_now_add=True, auto_now=False)
	updated = models.DateTimeField("Запис оновлено", auto_now_add=False, auto_now=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return "Замовлення %s %s %s" % (self.id, self.invoice, self.provider)
	class Meta:
		verbose_name = 'Замовлення матеріалу, чорнила, іншого'
		verbose_name_plural = 'Замовлення матеріалів, чорнил, іншого'
