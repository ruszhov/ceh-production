from django.shortcuts import render

from django.utils import timezone
import datetime
import decimal
from datetime import timedelta, date
from django.http import HttpResponse
from printorder.models import *
from django.db.models import Sum
import json
from django.db.models.functions import TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond


def printstatistics(request):
    return render(request, 'printstatistics/printstatistics.html', locals())

def printstatistics_bbs(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

	# all_bbs_by_days = PrintOrder.objects.all()\
	all_bbs_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_days)

	days_list = list()
	bbs_by_days = dict()
	sitik_by_days = dict()
	scroll_by_days = dict()

	for order_by_days in all_bbs_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 1:
			if order_by_days["date_item"] in bbs_by_days:
				bbs_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				bbs_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 2:
			if order_by_days["date_item"] in sitik_by_days:
				sitik_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				sitik_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 9:
			if order_by_days["date_item"] in scroll_by_days:
				scroll_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				scroll_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	bbs_by_days_data = list()
	for day_item in days_list:
		if day_item in bbs_by_days:
			bbs_by_days_data.append(bbs_by_days[day_item])
		else:
			bbs_by_days_data.append(0)

	sitik_by_days_data = list()
	for day_item in days_list:
		if day_item in sitik_by_days:
			sitik_by_days_data.append(sitik_by_days[day_item])
		else:
			sitik_by_days_data.append(0)

	scroll_by_days_data = list()
	for day_item in days_list:
		if day_item in scroll_by_days:
			scroll_by_days_data.append(scroll_by_days[day_item])
		else:
			scroll_by_days_data.append(0)

	all_bbs_by_days_data = dict()
	all_bbs_by_days_data["chart_print"] = dict()
	all_bbs_by_days_data["chart_print"]["days_list"] = days_list
	all_bbs_by_days_data["chart_print"]["series"] = [
		{"name": "Блюбек", "data": bbs_by_days_data},
		{"name": "Сітік", "data": sitik_by_days_data},
		{"name": "Скролл", "data": scroll_by_days_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_bbs = json.dumps(all_bbs_by_days_data, default=custom_serializer)

	# print (charts_data_bbs)

	return render(request, 'printstatistics/printstatistics_bbs.html', locals())

def printstatistics_baner(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)


	#all_baner_by_days = PrintOrder.objects.all()\
	all_baner_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_dates)
	days_list = list()
	baner_lam_by_days = dict()
	baner_lyt_by_days = dict()
	baner_sitka_by_days = dict()
	beklit_by_days = dict()

	for order_by_days in all_baner_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 3:
			if order_by_days["date_item"] in baner_lam_by_days:
				baner_lam_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lam_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 4:
			if order_by_days["date_item"] in baner_lyt_by_days:
				baner_lyt_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lyt_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 8:
			if order_by_days["date_item"] in baner_sitka_by_days:
				baner_sitka_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_sitka_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 5:
			if order_by_days["date_item"] in beklit_by_days:
				beklit_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				beklit_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	baner_lam_by_days_data = list()
	for day_item in days_list:
		if day_item in baner_lam_by_days:
			baner_lam_by_days_data.append(baner_lam_by_days[day_item])
		else:
			baner_lam_by_days_data.append(0)

	baner_lyt_by_days_data = list()
	for day_item in days_list:
		if day_item in baner_lyt_by_days:
			baner_lyt_by_days_data.append(baner_lyt_by_days[day_item])
		else:
			baner_lyt_by_days_data.append(0)

	baner_sitka_by_days_data = list()
	for day_item in days_list:
		if day_item in baner_sitka_by_days:
			baner_sitka_by_days_data.append(baner_sitka_by_days[day_item])
		else:
			baner_sitka_by_days_data.append(0)

	beklit_by_days_data = list()
	for day_item in days_list:
		if day_item in beklit_by_days:
			beklit_by_days_data.append(beklit_by_days[day_item])
		else:
			beklit_by_days_data.append(0)

	all_baner_by_days_data = dict()
	all_baner_by_days_data["chart_print"] = dict()
	all_baner_by_days_data["chart_print"]["days_list"] = days_list
	all_baner_by_days_data["chart_print"]["series"] = [
		{"name": "Банер ламінований", "data": baner_lam_by_days_data},
		{"name": "Банер литий", "data": baner_lyt_by_days_data},
		{"name": "Банерна сітка", "data": baner_sitka_by_days_data},
		{"name": "Бекліт", "data": beklit_by_days_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_baner.html', locals())

def printstatistics_oracal(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

	# all_oracal_by_days = PrintOrder.objects.all()\
	all_oracal_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_dates)
	days_list = list()
	orah_by_days = dict()
	oram_by_days = dict()

	for order_by_days in all_oracal_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 6:
			if order_by_days["date_item"] in orah_by_days:
				orah_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				orah_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 7:
			if order_by_days["date_item"] in oram_by_days:
				oram_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				oram_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	orah_by_days_data = list()
	for day_item in days_list:
		if day_item in orah_by_days:
			orah_by_days_data.append(orah_by_days[day_item])
		else:
			orah_by_days_data.append(0)

	oram_by_days_data = list()
	for day_item in days_list:
		if day_item in oram_by_days:
			oram_by_days_data.append(oram_by_days[day_item])
		else:
			oram_by_days_data.append(0)

	all_oracal_by_days_data = dict()
	all_oracal_by_days_data["chart_print"] = dict()
	all_oracal_by_days_data["chart_print"]["days_list"] = days_list
	all_oracal_by_days_data["chart_print"]["series"] = [
		{"name": "Оракал глянцевий", "data": orah_by_days_data},
		{"name": "Оракал матовий", "data": oram_by_days_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_oracal = json.dumps(all_oracal_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_oracal.html', locals())

def printstatistics_holst(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

	# all_holst_by_days = PrintOrder.objects.all()\
	all_holst_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_dates)
	days_list = list()
	photo_by_days = dict()
	holst_by_days = dict()

	for order_by_days in all_holst_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 10:
			if order_by_days["date_item"] in photo_by_days:
				photo_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				photo_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 11:
			if order_by_days["date_item"] in holst_by_days:
				holst_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				holst_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	photo_by_days_data = list()
	for day_item in days_list:
		if day_item in photo_by_days:
			photo_by_days_data.append(photo_by_days[day_item])
		else:
			photo_by_days_data.append(0)

	holst_by_days_data = list()
	for day_item in days_list:
		if day_item in holst_by_days:
			holst_by_days_data.append(holst_by_days[day_item])
		else:
			holst_by_days_data.append(0)

	all_holst_by_days_data = dict()
	all_holst_by_days_data["chart_print"] = dict()
	all_holst_by_days_data["chart_print"]["days_list"] = days_list
	all_holst_by_days_data["chart_print"]["series"] = [
		{"name": "Фотошпалери", "data": photo_by_days_data},
		{"name": "Холст", "data": holst_by_days_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_holst = json.dumps(all_holst_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_holst.html', locals())