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
	
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

	# all_bbs_by_days = PrintOrder.objects.all()\
	all_bbs_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	days_list = list()
	bbs_by_days = dict()
	# sitik_by_days = dict()
	# scroll_by_days = dict()

	for order_by_days in all_bbs_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 1:
			if order_by_days["date_item"] in bbs_by_days:
				bbs_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				bbs_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		
	bbs_by_days_data = list()
	for day_item in days_list:
		if day_item in bbs_by_days:
			bbs_by_days_data.append(bbs_by_days[day_item])
		else:
			bbs_by_days_data.append(0)

	all_bbs_by_days_data = dict()
	all_bbs_by_days_data["chart_print"] = dict()
	all_bbs_by_days_data["chart_print"]["days_list"] = days_list
	all_bbs_by_days_data["chart_print"]["series"] = [
		{"name": "Блюбек 1.56м", "data": bbs_by_days_data},
		# {"name": "Сітік", "data": sitik_by_days_data},
		# {"name": "Скролл", "data": scroll_by_days_data},
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


def printstatistics_baner_lam(request):
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
	baner_lam_by_days_137 = dict()
	baner_lam_by_days_16 = dict()
	baner_lam_by_days_22 = dict()
	baner_lam_by_days_25 = dict()
	baner_lam_by_days_32 = dict()

	for order_by_days in all_baner_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 3:
			if order_by_days["date_item"] in baner_lam_by_days_137:
				baner_lam_by_days_137[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lam_by_days_137[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 22:
			if order_by_days["date_item"] in baner_lam_by_days_16:
				baner_lam_by_days_16[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lam_by_days_16[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 21:
			if order_by_days["date_item"] in baner_lam_by_days_22:
				baner_lam_by_days_22[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lam_by_days_22[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 20:
			if order_by_days["date_item"] in baner_lam_by_days_25:
				baner_lam_by_days_25[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lam_by_days_25[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 19:
			if order_by_days["date_item"] in baner_lam_by_days_32:
				baner_lam_by_days_32[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lam_by_days_32[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	baner_lam_by_days_data_137 = list()
	for day_item in days_list:
		if day_item in baner_lam_by_days_137:
			baner_lam_by_days_data_137.append(baner_lam_by_days_137[day_item])
		else:
			baner_lam_by_days_data_137.append(0)

	baner_lam_by_days_data_16 = list()
	for day_item in days_list:
		if day_item in baner_lam_by_days_16:
			baner_lam_by_days_data_16.append(baner_lam_by_days_16[day_item])
		else:
			baner_lam_by_days_data_16.append(0)

	baner_lam_by_days_data_22 = list()
	for day_item in days_list:
		if day_item in baner_lam_by_days_22:
			baner_lam_by_days_data_22.append(baner_lam_by_days_22[day_item])
		else:
			baner_lam_by_days_data_22.append(0)

	baner_lam_by_days_data_25 = list()
	for day_item in days_list:
		if day_item in baner_lam_by_days_25:
			baner_lam_by_days_data_25.append(baner_lam_by_days_25[day_item])
		else:
			baner_lam_by_days_data_25.append(0)

	baner_lam_by_days_data_32 = list()
	for day_item in days_list:
		if day_item in baner_lam_by_days_32:
			baner_lam_by_days_data_32.append(baner_lam_by_days_32[day_item])
		else:
			baner_lam_by_days_data_32.append(0)

	all_baner_by_days_data = dict()
	all_baner_by_days_data["chart_print"] = dict()
	all_baner_by_days_data["chart_print"]["days_list"] = days_list
	all_baner_by_days_data["chart_print"]["series"] = [
		{"name": "Банер ламінований 1.37м", "data": baner_lam_by_days_data_137},
		{"name": "Банер ламінований 1.6м", "data": baner_lam_by_days_data_16},
		{"name": "Банер ламінований 2.2м", "data": baner_lam_by_days_data_22},
		{"name": "Банер ламінований 2.5м", "data": baner_lam_by_days_data_25},
		{"name": "Банер ламінований 3.2м", "data": baner_lam_by_days_data_32},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_baner_lam.html', locals())

def printstatistics_baner_lyt(request):
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
	baner_lyt_by_days_16 = dict()
	baner_lyt_by_days_22 = dict()
	baner_lyt_by_days_25 = dict()
	baner_lyt_by_days_32 = dict()

	for order_by_days in all_baner_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 29:
			if order_by_days["date_item"] in baner_lyt_by_days_16:
				baner_lyt_by_days_16[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lyt_by_days_16[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 16:
			if order_by_days["date_item"] in baner_lyt_by_days_22:
				baner_lyt_by_days_22[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lyt_by_days_22[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 15:
			if order_by_days["date_item"] in baner_lyt_by_days_25:
				baner_lyt_by_days_25[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lyt_by_days_25[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 4:
			if order_by_days["date_item"] in baner_lyt_by_days_32:
				baner_lyt_by_days_32[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lyt_by_days_32[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	baner_lyt_by_days_data_16 = list()
	for day_item in days_list:
		if day_item in baner_lyt_by_days_16:
			baner_lyt_by_days_data_16.append(baner_lyt_by_days_16[day_item])
		else:
			baner_lyt_by_days_data_16.append(0)

	baner_lyt_by_days_data_22 = list()
	for day_item in days_list:
		if day_item in baner_lyt_by_days_22:
			baner_lyt_by_days_data_22.append(baner_lyt_by_days_22[day_item])
		else:
			baner_lyt_by_days_data_22.append(0)

	baner_lyt_by_days_data_25 = list()
	for day_item in days_list:
		if day_item in baner_lyt_by_days_25:
			baner_lyt_by_days_data_25.append(baner_lyt_by_days_25[day_item])
		else:
			baner_lyt_by_days_data_25.append(0)

	baner_lyt_by_days_data_32 = list()
	for day_item in days_list:
		if day_item in baner_lyt_by_days_32:
			baner_lyt_by_days_data_32.append(baner_lyt_by_days_32[day_item])
		else:
			baner_lyt_by_days_data_32.append(0)

	all_baner_by_days_data = dict()
	all_baner_by_days_data["chart_print"] = dict()
	all_baner_by_days_data["chart_print"]["days_list"] = days_list
	all_baner_by_days_data["chart_print"]["series"] = [
		{"name": "Банер литий 1.6м", "data": baner_lyt_by_days_data_16},
		{"name": "Банер литий 2.2м", "data": baner_lyt_by_days_data_22},
		{"name": "Банер литий 2.5м", "data": baner_lyt_by_days_data_25},
		{"name": "Банер литий 3.2м", "data": baner_lyt_by_days_data_32},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_baner_lyt.html', locals())

def printstatistics_baner_sitka(request):
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
	baner_sitka_by_days_22 = dict()
	baner_sitka_by_days_25 = dict()
	baner_sitka_by_days_32 = dict()

	for order_by_days in all_baner_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 23:
			if order_by_days["date_item"] in baner_sitka_by_days_22:
				baner_sitka_by_days_22[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_sitka_by_days_22[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 24:
			if order_by_days["date_item"] in baner_sitka_by_days_25:
				baner_sitka_by_days_25[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_sitka_by_days_25[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 8:
			if order_by_days["date_item"] in baner_sitka_by_days_32:
				baner_sitka_by_days_32[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_sitka_by_days_32[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	baner_sitka_by_days_data_22 = list()
	for day_item in days_list:
		if day_item in baner_sitka_by_days_22:
			baner_sitka_by_days_data_22.append(baner_sitka_by_days_22[day_item])
		else:
			baner_sitka_by_days_data_22.append(0)

	baner_sitka_by_days_data_25 = list()
	for day_item in days_list:
		if day_item in baner_sitka_by_days_25:
			baner_sitka_by_days_data_25.append(baner_sitka_by_days_25[day_item])
		else:
			baner_sitka_by_days_data_25.append(0)

	baner_sitka_by_days_data_32 = list()
	for day_item in days_list:
		if day_item in baner_sitka_by_days_32:
			baner_sitka_by_days_data_32.append(baner_sitka_by_days_32[day_item])
		else:
			baner_sitka_by_days_data_32.append(0)

	all_baner_by_days_data = dict()
	all_baner_by_days_data["chart_print"] = dict()
	all_baner_by_days_data["chart_print"]["days_list"] = days_list
	all_baner_by_days_data["chart_print"]["series"] = [
		{"name": "Банерна сітка 2.2м", "data": baner_sitka_by_days_data_22},
		{"name": "Банерна сітка 2.5м", "data": baner_sitka_by_days_data_25},
		{"name": "Банерна сітка 3.2м", "data": baner_sitka_by_days_data_32},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_baner_sitka.html', locals())

def printstatistics_beklit(request):
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
	baner_beklit_by_days_22 = dict()
	baner_beklit_by_days_25 = dict()
	baner_beklit_by_days_32 = dict()

	for order_by_days in all_baner_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 18:
			if order_by_days["date_item"] in baner_beklit_by_days_22:
				baner_beklit_by_days_22[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_beklit_by_days_22[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 17:
			if order_by_days["date_item"] in baner_beklit_by_days_25:
				baner_beklit_by_days_25[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_beklit_by_days_25[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 5:
			if order_by_days["date_item"] in baner_beklit_by_days_32:
				baner_beklit_by_days_32[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_beklit_by_days_32[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	baner_beklit_by_days_data_22 = list()
	for day_item in days_list:
		if day_item in baner_beklit_by_days_22:
			baner_beklit_by_days_data_22.append(baner_beklit_by_days_22[day_item])
		else:
			baner_beklit_by_days_data_22.append(0)

	baner_beklit_by_days_data_25 = list()
	for day_item in days_list:
		if day_item in baner_beklit_by_days_25:
			baner_beklit_by_days_data_25.append(baner_beklit_by_days_25[day_item])
		else:
			baner_beklit_by_days_data_25.append(0)

	baner_beklit_by_days_data_32 = list()
	for day_item in days_list:
		if day_item in baner_beklit_by_days_32:
			baner_beklit_by_days_data_32.append(baner_beklit_by_days_32[day_item])
		else:
			baner_beklit_by_days_data_32.append(0)

	all_baner_by_days_data = dict()
	all_baner_by_days_data["chart_print"] = dict()
	all_baner_by_days_data["chart_print"]["days_list"] = days_list
	all_baner_by_days_data["chart_print"]["series"] = [
		{"name": "Бекліт 2.2м", "data": baner_beklit_by_days_data_22},
		{"name": "Бекліт 2.5м", "data": baner_beklit_by_days_data_25},
		{"name": "Бекліт 3.2м", "data": baner_beklit_by_days_data_32},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_beklit.html', locals())

def printstatistics_oracal_gl(request):
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
	orah_by_days_137 = dict()
	orah_by_days_126 = dict()
	orah_by_days_1 = dict()

	for order_by_days in all_oracal_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 27:
			if order_by_days["date_item"] in orah_by_days_1:
				orah_by_days_1[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				orah_by_days_1[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 31:
			if order_by_days["date_item"] in orah_by_days_126:
				orah_by_days_126[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				orah_by_days_126[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 6:
			if order_by_days["date_item"] in orah_by_days_137:
				orah_by_days_137[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				orah_by_days_137[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	orah_by_days_137_data = list()
	for day_item in days_list:
		if day_item in orah_by_days_137:
			orah_by_days_137_data.append(orah_by_days_137[day_item])
		else:
			orah_by_days_137_data.append(0)

	orah_by_days_126_data = list()
	for day_item in days_list:
		if day_item in orah_by_days_126:
			orah_by_days_126_data.append(orah_by_days_126[day_item])
		else:
			orah_by_days_126_data.append(0)

	orah_by_days_1_data = list()
	for day_item in days_list:
		if day_item in orah_by_days_1:
			orah_by_days_1_data.append(orah_by_days_1[day_item])
		else:
			orah_by_days_1_data.append(0)

	all_oracal_by_days_data = dict()
	all_oracal_by_days_data["chart_print"] = dict()
	all_oracal_by_days_data["chart_print"]["days_list"] = days_list
	all_oracal_by_days_data["chart_print"]["series"] = [
		{"name": "Оракал глянцевий 1м", "data": orah_by_days_1_data},
		{"name": "Оракал глянцевий 1.26м", "data": orah_by_days_126_data},
		{"name": "Оракал глянцевий 1,37м", "data": orah_by_days_137_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_oracal = json.dumps(all_oracal_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_oracal_gl.html', locals())

def printstatistics_oracal_mat(request):
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
	oram_by_days_137 = dict()
	oram_by_days_126 = dict()
	oram_by_days_1 = dict()

	for order_by_days in all_oracal_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 28:
			if order_by_days["date_item"] in oram_by_days_1:
				oram_by_days_1[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				oram_by_days_1[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 32:
			if order_by_days["date_item"] in oram_by_days_126:
				oram_by_days_126[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				oram_by_days_126[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 7:
			if order_by_days["date_item"] in oram_by_days_137:
				oram_by_days_137[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				oram_by_days_137[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	oram_by_days_137_data = list()
	for day_item in days_list:
		if day_item in oram_by_days_137:
			oram_by_days_137_data.append(oram_by_days_137[day_item])
		else:
			oram_by_days_137_data.append(0)

	oram_by_days_126_data = list()
	for day_item in days_list:
		if day_item in oram_by_days_126:
			oram_by_days_126_data.append(oram_by_days_126[day_item])
		else:
			oram_by_days_126_data.append(0)

	oram_by_days_1_data = list()
	for day_item in days_list:
		if day_item in oram_by_days_1:
			oram_by_days_1_data.append(oram_by_days_1[day_item])
		else:
			oram_by_days_1_data.append(0)

	all_oracal_by_days_data = dict()
	all_oracal_by_days_data["chart_print"] = dict()
	all_oracal_by_days_data["chart_print"]["days_list"] = days_list
	all_oracal_by_days_data["chart_print"]["series"] = [
		{"name": "Оракал матовий 1м", "data": oram_by_days_1_data},
		{"name": "Оракал матовий 1.26м", "data": oram_by_days_126_data},
		{"name": "Оракал матовий 1,37м", "data": oram_by_days_137_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_oracal = json.dumps(all_oracal_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_oracal_mat.html', locals())

def printstatistics_scroll(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

	# all_oracal_by_days = PrintOrder.objects.all()\
	all_scroll_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_dates)
	days_list = list()
	scroll_by_days_127 = dict()
	scroll_by_days_315 = dict()

	for order_by_days in all_scroll_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 14:
			if order_by_days["date_item"] in scroll_by_days_127:
				scroll_by_days_127[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				scroll_by_days_127[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 9:
			if order_by_days["date_item"] in scroll_by_days_315:
				scroll_by_days_315[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				scroll_by_days_315[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	scroll_by_days_127_data = list()
	for day_item in days_list:
		if day_item in scroll_by_days_127:
			scroll_by_days_127_data.append(scroll_by_days_127[day_item])
		else:
			scroll_by_days_127_data.append(0)

	scroll_by_days_315_data = list()
	for day_item in days_list:
		if day_item in scroll_by_days_315:
			scroll_by_days_315_data.append(scroll_by_days_315[day_item])
		else:
			scroll_by_days_315_data.append(0)

	all_scroll_by_days_data = dict()
	all_scroll_by_days_data["chart_print"] = dict()
	all_scroll_by_days_data["chart_print"]["days_list"] = days_list
	all_scroll_by_days_data["chart_print"]["series"] = [
		{"name": "Скролл 1.27м", "data": scroll_by_days_127_data},
		{"name": "Скролл 3,15м", "data": scroll_by_days_315_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_scroll = json.dumps(all_scroll_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_scroll.html', locals())

def printstatistics_sitik(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)


	#all_baner_by_days = PrintOrder.objects.all()\
	all_sitik_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_dates)
	days_list = list()
	sitik_by_days_125 = dict()
	sitik_by_days_127 = dict()
	sitik_by_days_16 = dict()

	for order_by_days in all_sitik_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 25:
			if order_by_days["date_item"] in sitik_by_days_125:
				sitik_by_days_125[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				sitik_by_days_125[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 2:
			if order_by_days["date_item"] in sitik_by_days_127:
				sitik_by_days_127[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				sitik_by_days_127[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 26:
			if order_by_days["date_item"] in sitik_by_days_16:
				sitik_by_days_16[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				sitik_by_days_16[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	sitik_by_days_data_125 = list()
	for day_item in days_list:
		if day_item in sitik_by_days_125:
			sitik_by_days_data_125.append(sitik_by_days_125[day_item])
		else:
			sitik_by_days_data_125.append(0)

	sitik_by_days_data_127 = list()
	for day_item in days_list:
		if day_item in sitik_by_days_127:
			sitik_by_days_data_127.append(sitik_by_days_127[day_item])
		else:
			sitik_by_days_data_127.append(0)

	sitik_by_days_data_16 = list()
	for day_item in days_list:
		if day_item in sitik_by_days_16:
			sitik_by_days_data_16.append(sitik_by_days_16[day_item])
		else:
			sitik_by_days_data_16.append(0)

	all_sitik_by_days_data = dict()
	all_sitik_by_days_data["chart_print"] = dict()
	all_sitik_by_days_data["chart_print"]["days_list"] = days_list
	all_sitik_by_days_data["chart_print"]["series"] = [
		{"name": "Сітік 1.25м", "data": sitik_by_days_data_125},
		{"name": "Сітік 1.27м", "data": sitik_by_days_data_127},
		{"name": "Сітік 1.6м", "data": sitik_by_days_data_16},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_sitik = json.dumps(all_sitik_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_sitik.html', locals())

def printstatistics_photo(request):
	# user=request.user
	# if not user.is_superuser:
	# 	return HttpResponseRedirect(reverse('home'))
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

	# all_oracal_by_days = PrintOrder.objects.all()\
	all_photo_by_days = PrintOrder.objects.filter(created__range=[startdate, enddate])\
		.annotate(date_item=TruncDate('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# print (all_bbs_by_dates)
	days_list = list()
	photos_by_days = dict()
	photop_by_days = dict()

	for order_by_days in all_photo_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 10:
			if order_by_days["date_item"] in photos_by_days:
				photos_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				photos_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 12:
			if order_by_days["date_item"] in photop_by_days:
				photop_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				photop_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	photos_by_days_data = list()
	for day_item in days_list:
		if day_item in photos_by_days:
			photos_by_days_data.append(photos_by_days[day_item])
		else:
			photos_by_days_data.append(0)

	photop_by_days_data = list()
	for day_item in days_list:
		if day_item in photop_by_days:
			photop_by_days_data.append(photop_by_days[day_item])
		else:
			photop_by_days_data.append(0)

	all_photo_by_days_data = dict()
	all_photo_by_days_data["chart_print"] = dict()
	all_photo_by_days_data["chart_print"]["days_list"] = days_list
	all_photo_by_days_data["chart_print"]["series"] = [
		{"name": "Фотошпалери", "data": photos_by_days_data},
		{"name": "Фотопапір 1.07м", "data": photop_by_days_data},
	]

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_photo = json.dumps(all_photo_by_days_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_photo.html', locals())

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
	onevision_by_days = dict()
	poliman_by_days = dict()
	holst_by_days = dict()

	for order_by_days in all_holst_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 13:
			if order_by_days["date_item"] in onevision_by_days:
				onevision_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				onevision_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 30:
			if order_by_days["date_item"] in poliman_by_days:
				poliman_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				poliman_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 11:
			if order_by_days["date_item"] in holst_by_days:
				holst_by_days[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				holst_by_days[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

	# print (days_list)
	# print (bbs_by_days)

	onevision_by_days_data = list()
	for day_item in days_list:
		if day_item in onevision_by_days:
			onevision_by_days_data.append(onevision_by_days[day_item])
		else:
			onevision_by_days_data.append(0)

	poliman_by_days_data = list()
	for day_item in days_list:
		if day_item in poliman_by_days:
			poliman_by_days_data.append(poliman_by_days[day_item])
		else:
			poliman_by_days_data.append(0)

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
		{"name": "Ван віжн", "data": onevision_by_days_data},
		{"name": "Поліман 1.27м", "data": poliman_by_days_data},
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