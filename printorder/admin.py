from django.contrib import admin
from .models import *
# Register your models here.

class PrintOrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PrintOrder._meta.fields]
	search_fields = ['name_of_camp', 'image_url', 'manager']

	class Meta:
		model = PrintOrder
admin.site.register(PrintOrder, PrintOrderAdmin)

class MaterialAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Material._meta.fields]
	search_fields = ['name_of_material']

	class Meta:
		model=  Material
admin.site.register(Material, MaterialAdmin)

class OfficeManagerAdmin(admin.ModelAdmin):
	list_display = [field.name for field in OfficeManager._meta.fields]

	class Meta:
		model = OfficeManager
admin.site.register(OfficeManager, OfficeManagerAdmin)

class CampaignNameAdmin(admin.ModelAdmin):
	list_display = [field.name for field in CampaignName._meta.fields]
	search_fields = ['name_of_new_camp']

	class Meta:
		model = CampaignName
admin.site.register(CampaignName, CampaignNameAdmin)

class PrintStatusAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PrintStatus._meta.fields]

	class Meta:
		model = PrintStatus
admin.site.register(PrintStatus, PrintStatusAdmin)