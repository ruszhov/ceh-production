from django.contrib import admin
from .models import *
# Register your models here.

class PrintersAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Printers._meta.fields]
	search_fields = ['name']

	class Meta:
		model = Printers
admin.site.register(Printers, PrintersAdmin)

class PrintLogAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PrintLog._meta.fields]
	search_fields = ['name']

	class Meta:
		model=  PrintLog
admin.site.register(PrintLog, PrintLogAdmin)

class RipLogAdmin(admin.ModelAdmin):
	list_display = [field.name for field in RipLog._meta.fields]
	search_fields = ['name']

	class Meta:
		model=RipLog
admin.site.register(RipLog, RipLogAdmin)