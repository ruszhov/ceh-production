from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
	name_of_material = models.CharField(max_length=50)
	description = models.CharField(max_length=50, blank=True)
	total_m_kv_per_month = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
	total_m_kv = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)

	def __str__(self):
		return self.name_of_material

	class Meta:
		verbose_name = 'Матеріал'
		verbose_name_plural = 'Матеріали'
		ordering = ['name_of_material']

class OfficeManager(models.Model):
	name_of_manager = models.CharField(max_length=30)
	description = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name_of_manager

	class Meta:
		verbose_name = 'Менеджер'
		verbose_name_plural = 'Менеджери'
		ordering = ['name_of_manager']

class PrintStatus(models.Model):
	status = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return self.status
	class Meta:
		verbose_name = 'Статус друку'
		verbose_name_plural = 'Статуси друку'
		ordering = ['status']

class CampaignName(models.Model):
	name_of_new_camp = models.CharField(max_length=50, unique=True, error_messages={'unique':u"Сюжет з таким іменем вже існує в системі!"})
	description = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.name_of_new_camp

	class Meta:
		verbose_name = 'Кампанія'
		verbose_name_plural = 'Кампанії'
		ordering = ['name_of_new_camp']

class DoneSteps(models.Model):
	tmp_number = models.IntegerField(null=True, default=None)
	print_order = models.ForeignKey('printorder.PrintOrder',  blank=True, null=True, related_name="printorder_comments", on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='tmp_created_by', default=None, null=True)
	updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='tmp_updated_by', default=None, null=True)

	def __str__(self):
		return "%s %s" % (self.tmp_number, self.created_by)
	class Meta:
		verbose_name = 'Етап виконання'
		verbose_name_plural = 'Етапи виконання'


class PrintOrder(models.Model):
	name_of_camp = models.ForeignKey(CampaignName, blank=False, null=False, default=None, on_delete = models.DO_NOTHING,)
	#image_url = models.URLField()
	#image_url_1 = models.URLField(max_length=200, blank=False, default=None)
	#image_url = models.ImageField()
	image_url = models.CharField(max_length=200, blank=False)
	# prioritet = models.BooleanField(default=False)
	STATUS_CHOICES = (("NO", "Ні"), ("YES", "Так"))
	prioritet = models.CharField(max_length=9, choices=STATUS_CHOICES, default='1')
	material = models.ForeignKey(Material, blank=False, null=True, default=None, on_delete = models.DO_NOTHING,)
	print_width = models.FloatField(null=True)
	print_height = models.FloatField(null=True)
	number = models.IntegerField(null=False, default=None)
	m_kv = models.DecimalField(max_digits=9, decimal_places=3, null=True)
	manager = models.ForeignKey(OfficeManager, null=True, default=None, on_delete = models.DO_NOTHING,)
	description = models.TextField(max_length=100, blank=True)
	status = models.ForeignKey(PrintStatus, blank=True, null=True, default=None, on_delete = models.DO_NOTHING,)
	created_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='created_by', default=None, null=True)
	updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='updated_by', default=None, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	# updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	updated = models.DateTimeField(null=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return "Замовлення %s %s" % (self.id, self.name_of_camp.name_of_new_camp)
	class Meta:
		verbose_name = 'Замовлення друку'
		verbose_name_plural = 'Список замовлень друку'