from django.contrib import admin
from .models import *

class ProviderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Provider._meta.fields]

	class Meta:
		model = Provider
admin.site.register(Provider, ProviderAdmin)

class MaterialInAdmin(admin.ModelAdmin):
	list_display = [field.name for field in MaterialIn._meta.fields]

	class Meta:
		model = MaterialIn
admin.site.register(MaterialIn, MaterialInAdmin)

class PaintInAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PaintIn._meta.fields]

	class Meta:
		model = PaintIn
admin.site.register(PaintIn, PaintInAdmin)

class OtherInAdmin(admin.ModelAdmin):
	list_display = [field.name for field in OtherIn._meta.fields]

	class Meta:
		model = OtherIn
admin.site.register(OtherIn, OtherInAdmin)

class MaterialOrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in MaterialOrder._meta.fields]

	class Meta:
		model = MaterialOrder
admin.site.register(MaterialOrder, MaterialOrderAdmin)

