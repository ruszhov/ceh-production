from django.shortcuts import render

from django.utils import timezone
import datetime
import decimal
from datetime import timedelta, date
from django.http import HttpResponse
from printorder.models import *
from materialorder.models import *
from django.db.models import Sum
import json
from django.db.models.functions import TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond
from django.db.models.functions import ExtractMonth


def printstatistics(request):
    return render(request, 'printstatistics/printstatistics.html', locals())

def printstatistics_bbs(request):
	
	# datetime.datetime.now(tz=timezone.utc)
	# enddate = datetime.date.today() + timedelta(days = 1)
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

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)
	# startmonth = datetime.ye

	# all_bbs_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
	all_bbs_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	# all_bbs_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
	all_bbs_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")
	# print(all_bbs_by_months)

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	months_list = list()
	bbs_by_months = dict()
	bbs_by_months_in = dict()

	for order_by_months in all_bbs_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 1:
			if order_by_months["date_item"] in bbs_by_months:
				bbs_by_months[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				bbs_by_months[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_bbs_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 2:
			if order_by_months_in["date_item"] in bbs_by_months_in:
				bbs_by_months_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				bbs_by_months_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	bbs_by_months_data = list()
	for month_item in months_list:
		if month_item in bbs_by_months:
			bbs_by_months_data.append(bbs_by_months[month_item])
		else:
			bbs_by_months_data.append(0)

	bbs_by_months_data_in = list()
	for month_item in months_list:
		if month_item in bbs_by_months_in:
			bbs_by_months_data_in.append(bbs_by_months_in[month_item])
		else:
			bbs_by_months_data_in.append(0)

	# months = {yan:'Січень', feb:'Лютий', mar:'Березень', apr:'Квітень', mai:'Травень', jun:'Червень', jul:'Липень', aug:'Серпень', sep:'Вересень', okt:'Жовтень', nov:'Листопад',dec:'Грудень'}
	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад', 12:'Грудень'}
	# for month in months_list:
	# 	if not month["month_item"]
	months_list = [months.get(n, n) for n in months_list]
	# print(months_list)
	# print(months_list)

	all_bbs_by_months_data = dict()
	all_bbs_by_months_data["chart_print"] = dict()
	all_bbs_by_months_data["chart_print"]["months_list"] = months_list
	all_bbs_by_months_data["chart_print"]["months_series"] = [

		{"name": "Блюбек 1.56м (використано)", "data": bbs_by_months_data, "pointPadding": 0.3, "pointPlacement": 0.0},
		{"name": "Блюбек 1.56м (надійшло)", "data": bbs_by_months_data_in, "pointPadding": 0.4, "pointPlacement": 0.0},
	]
	# print(all_bbs_by_months_data)

	#End filtering by months ####################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_bbs = json.dumps(all_bbs_by_days_data, default=custom_serializer)
	# print(charts_data_bbs)
	charts_data_bbs_months = json.dumps(all_bbs_by_months_data, default=custom_serializer)

	return render(request, 'printstatistics/printstatistics_bbs.html', locals())


def printstatistics_baner_lam(request):
		
	enddate = datetime.date.today() + timedelta(days = 1)
	startdate = enddate - timedelta(days=31)

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

	# print(all_baner_by_days_data)

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_baner_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_baner_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	baner_lam_by_months_137 = dict()
	baner_lam_by_months_16 = dict()
	baner_lam_by_months_22 = dict()
	baner_lam_by_months_25 = dict()
	baner_lam_by_months_32 = dict()

	baner_lam_by_months_137_in = dict()
	baner_lam_by_months_16_in = dict()
	baner_lam_by_months_22_in = dict()
	baner_lam_by_months_25_in = dict()
	baner_lam_by_months_32_in = dict()

	for order_by_months in all_baner_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 3:
			if order_by_months["date_item"] in baner_lam_by_months_137:
				baner_lam_by_months_137[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lam_by_months_137[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 22:
			if order_by_months["date_item"] in baner_lam_by_months_16:
				baner_lam_by_months_16[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lam_by_months_16[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 21:
			if order_by_months["date_item"] in baner_lam_by_months_22:
				baner_lam_by_months_22[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lam_by_months_22[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 20:
			if order_by_months["date_item"] in baner_lam_by_months_25:
				baner_lam_by_months_25[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lam_by_months_25[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 19:
			if order_by_months["date_item"] in baner_lam_by_months_32:
				baner_lam_by_months_32[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lam_by_months_32[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_baner_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 14:
			if order_by_months_in["date_item"] in baner_lam_by_months_137_in:
				baner_lam_by_months_137_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lam_by_months_137_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 13:
			if order_by_months_in["date_item"] in baner_lam_by_months_16_in:
				baner_lam_by_months_16_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lam_by_months_16_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 28:
			if order_by_months_in["date_item"] in baner_lam_by_months_22_in:
				baner_lam_by_months_22_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lam_by_months_22_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 12:
			if order_by_months_in["date_item"] in baner_lam_by_months_25_in:
				baner_lam_by_months_25_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lam_by_months_25_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 11:
			if order_by_months_in["date_item"] in baner_lam_by_months_32_in:
				baner_lam_by_months_32_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lam_by_months_32_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]


	baner_lam_by_months_data_137 = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_137:
			baner_lam_by_months_data_137.append(baner_lam_by_months_137[month_item])
		else:
			baner_lam_by_months_data_137.append(0)

	baner_lam_by_months_data_16 = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_16:
			baner_lam_by_months_data_16.append(baner_lam_by_months_16[month_item])
		else:
			baner_lam_by_months_data_16.append(0)

	baner_lam_by_months_data_22 = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_22:
			baner_lam_by_months_data_22.append(baner_lam_by_months_22[month_item])
		else:
			baner_lam_by_months_data_22.append(0)

	baner_lam_by_months_data_25 = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_25:
			baner_lam_by_months_data_25.append(baner_lam_by_months_25[month_item])
		else:
			baner_lam_by_months_data_25.append(0)

	baner_lam_by_months_data_32 = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_32:
			baner_lam_by_months_data_32.append(baner_lam_by_months_32[month_item])
		else:
			baner_lam_by_months_data_32.append(0)



	baner_lam_by_months_data_137_in = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_137_in:
			baner_lam_by_months_data_137_in.append(baner_lam_by_months_137_in[month_item])
		else:
			baner_lam_by_months_data_137_in.append(0)

	baner_lam_by_months_data_16_in = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_16_in:
			baner_lam_by_months_data_16_in.append(baner_lam_by_months_16_in[month_item])
		else:
			baner_lam_by_months_data_16_in.append(0)

	baner_lam_by_months_data_22_in = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_22_in:
			baner_lam_by_months_data_22_in.append(baner_lam_by_months_22_in[month_item])
		else:
			baner_lam_by_months_data_22_in.append(0)

	baner_lam_by_months_data_25_in = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_25_in:
			baner_lam_by_months_data_25_in.append(baner_lam_by_months_25_in[month_item])
		else:
			baner_lam_by_months_data_25_in.append(0)

	baner_lam_by_months_data_32_in = list()
	for month_item in months_list:
		if month_item in baner_lam_by_months_32_in:
			baner_lam_by_months_data_32_in.append(baner_lam_by_months_32_in[month_item])
		else:
			baner_lam_by_months_data_32_in.append(0)


	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_baner_by_months_data = dict()
	all_baner_by_months_data["chart_print"] = dict()
	all_baner_by_months_data["chart_print"]["months_list"] = months_list
	all_baner_by_months_data["chart_print"]["months_series"] = [

		{"name": "Банер ламінований 1.37м (використано)", "data": baner_lam_by_months_data_137, "pointPadding": 0.36, "pointPlacement": -0.4, "color": "rgba(165,170,217,1)"},
		{"name": "Банер ламінований 1.37м (надійшло)", "data": baner_lam_by_months_data_137_in, "pointPadding": 0.42, "pointPlacement": -0.4, "color": "rgba(126,86,134,.9)"},

		{"name": "Банер ламінований 1.6м (використано)", "data": baner_lam_by_months_data_16, "pointPadding": 0.36, "pointPlacement": -0.2, "color": "rgba(248,161,63,1)"},
		{"name": "Банер ламінований 1.6м (надійшло)", "data": baner_lam_by_months_data_16_in, "pointPadding": 0.42, "pointPlacement": -0.2, "color": "rgba(186,60,61,.9)"},

		{"name": "Банер ламінований 2.2м (використано)", "data": baner_lam_by_months_data_22, "pointPadding": 0.36, "pointPlacement": 0.0, "color": "rgba(171,168,169,1)"},
		{"name": "Банер ламінований 2.2м (надійшло)", "data": baner_lam_by_months_data_22_in, "pointPadding": 0.42, "pointPlacement": 0.0, "color": "rgba(73,70,70,.9)"},
		
		{"name": "Банер ламінований 2.5м (використано)", "data": baner_lam_by_months_data_25, "pointPadding": 0.36, "pointPlacement": 0.2, "color": "rgba(138,255,174,1)"},
		{"name": "Банер ламінований 2.5м (надійшло)", "data": baner_lam_by_months_data_25_in, "pointPadding": 0.42, "pointPlacement": 0.2, "color": "rgba(29,130,60,.9)"},

		{"name": "Банер ламінований 3.2м (використано)", "data": baner_lam_by_months_data_32, "pointPadding": 0.36, "pointPlacement": 0.4, "color": "rgba(252,148,165,1)"},
		{"name": "Банер ламінований 3.2м (надійшло)", "data": baner_lam_by_months_data_32_in, "pointPadding": 0.42, "pointPlacement": 0.4, "color": "rgba(255,0,42,.9)"},
	]

	# print(all_baner_by_months_data)

	#End filtering by months ####################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	charts_data_baner_lam_months = json.dumps(all_baner_by_months_data, default=custom_serializer)

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
	baner_lyt_by_days_137 = dict()
	baner_lyt_by_days_16 = dict()
	baner_lyt_by_days_22 = dict()
	baner_lyt_by_days_25 = dict()
	baner_lyt_by_days_32 = dict()

	for order_by_days in all_baner_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 37:
			if order_by_days["date_item"] in baner_lyt_by_days_137:
				baner_lyt_by_days_137[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				baner_lyt_by_days_137[order_by_days["date_item"]] = order_by_days["m_kv_amount"]
				
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

	baner_lyt_by_days_data_137 = list()
	for day_item in days_list:
		if day_item in baner_lyt_by_days_137:
			baner_lyt_by_days_data_137.append(baner_lyt_by_days_137[day_item])
		else:
			baner_lyt_by_days_data_137.append(0)

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

		{"name": "Банер литий 1.37м", "data": baner_lyt_by_days_data_137},
		{"name": "Банер литий 1.6м", "data": baner_lyt_by_days_data_16},
		{"name": "Банер литий 2.2м", "data": baner_lyt_by_days_data_22},
		{"name": "Банер литий 2.5м", "data": baner_lyt_by_days_data_25},
		{"name": "Банер литий 3.2м", "data": baner_lyt_by_days_data_32},
	]

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_baner_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_baner_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	baner_lyt_by_months_137 = dict()
	baner_lyt_by_months_16 = dict()
	baner_lyt_by_months_22 = dict()
	baner_lyt_by_months_25 = dict()
	baner_lyt_by_months_32 = dict()

	baner_lyt_by_months_137_in = dict()
	baner_lyt_by_months_16_in = dict()
	baner_lyt_by_months_22_in = dict()
	baner_lyt_by_months_25_in = dict()
	baner_lyt_by_months_32_in = dict()

	# def add_order_by_months(dict, months_list, string, *args):
	# 	for order in dict:
	# 		if not order["date_item"] in months_list:
	# 			months_list.append(order["date_item"])
	# 		for i in args:
	# 			material = string + '_' + str(i)
	# 			if order["material_id"] == i:
	# 				if order["date_item"] in material:
	# 					material[order["date_item"]] += order["m_kv_amount"]
	# 				else:
	# 					material[order["date_item"]] = order["m_kv_amount"]


	for order_by_months in all_baner_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 37:
			if order_by_months["date_item"] in baner_lyt_by_months_137:
				baner_lyt_by_months_137[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lyt_by_months_137[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 29:
			if order_by_months["date_item"] in baner_lyt_by_months_16:
				baner_lyt_by_months_16[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lyt_by_months_16[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 16:
			if order_by_months["date_item"] in baner_lyt_by_months_22:
				baner_lyt_by_months_22[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lyt_by_months_22[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 15:
			if order_by_months["date_item"] in baner_lyt_by_months_25:
				baner_lyt_by_months_25[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lyt_by_months_25[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 4:
			if order_by_months["date_item"] in baner_lyt_by_months_32:
				baner_lyt_by_months_32[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_lyt_by_months_32[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_baner_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 38:
			if order_by_months_in["date_item"] in baner_lyt_by_months_137_in:
				baner_lyt_by_months_137_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lyt_by_months_137_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 25:
			if order_by_months_in["date_item"] in baner_lyt_by_months_16_in:
				baner_lyt_by_months_16_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lyt_by_months_16_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 7:
			if order_by_months_in["date_item"] in baner_lyt_by_months_22_in:
				baner_lyt_by_months_22_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lyt_by_months_22_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 6:
			if order_by_months_in["date_item"] in baner_lyt_by_months_25_in:
				baner_lyt_by_months_25_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lyt_by_months_25_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 5:
			if order_by_months_in["date_item"] in baner_lyt_by_months_32_in:
				baner_lyt_by_months_32_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_lyt_by_months_32_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]


	baner_lyt_by_months_data_137 = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_137:
			baner_lyt_by_months_data_137.append(baner_lyt_by_months_137[month_item])
		else:
			baner_lyt_by_months_data_137.append(0)

	baner_lyt_by_months_data_16 = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_16:
			baner_lyt_by_months_data_16.append(baner_lyt_by_months_16[month_item])
		else:
			baner_lyt_by_months_data_16.append(0)

	baner_lyt_by_months_data_22 = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_22:
			baner_lyt_by_months_data_22.append(baner_lyt_by_months_22[month_item])
		else:
			baner_lyt_by_months_data_22.append(0)

	baner_lyt_by_months_data_25 = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_25:
			baner_lyt_by_months_data_25.append(baner_lyt_by_months_25[month_item])
		else:
			baner_lyt_by_months_data_25.append(0)

	baner_lyt_by_months_data_32 = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_32:
			baner_lyt_by_months_data_32.append(baner_lyt_by_months_32[month_item])
		else:
			baner_lyt_by_months_data_32.append(0)



	baner_lyt_by_months_data_137_in = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_137_in:
			baner_lyt_by_months_data_137_in.append(baner_lyt_by_months_137_in[month_item])
		else:
			baner_lyt_by_months_data_137_in.append(0)

	baner_lyt_by_months_data_16_in = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_16_in:
			baner_lyt_by_months_data_16_in.append(baner_lyt_by_months_16_in[month_item])
		else:
			baner_lyt_by_months_data_16_in.append(0)

	baner_lyt_by_months_data_22_in = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_22_in:
			baner_lyt_by_months_data_22_in.append(baner_lyt_by_months_22_in[month_item])
		else:
			baner_lyt_by_months_data_22_in.append(0)

	baner_lyt_by_months_data_25_in = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_25_in:
			baner_lyt_by_months_data_25_in.append(baner_lyt_by_months_25_in[month_item])
		else:
			baner_lyt_by_months_data_25_in.append(0)

	baner_lyt_by_months_data_32_in = list()
	for month_item in months_list:
		if month_item in baner_lyt_by_months_32_in:
			baner_lyt_by_months_data_32_in.append(baner_lyt_by_months_32_in[month_item])
		else:
			baner_lyt_by_months_data_32_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_baner_by_months_data = dict()
	all_baner_by_months_data["chart_print"] = dict()
	all_baner_by_months_data["chart_print"]["months_list"] = months_list
	all_baner_by_months_data["chart_print"]["months_series"] = [

		{"name": "Банер литий 1.37м (використано)", "data": baner_lyt_by_months_data_137, "pointPadding": 0.36, "pointPlacement": -0.4, "color": "rgba(165,170,217,1)"},
		{"name": "Банер литий 1.37м (надійшло)", "data": baner_lyt_by_months_data_137_in, "pointPadding": 0.42, "pointPlacement": -0.4, "color": "rgba(126,86,134,.9)"},

		{"name": "Банер литий 1.6м (використано)", "data": baner_lyt_by_months_data_16, "pointPadding": 0.36, "pointPlacement": -0.2, "color": "rgba(248,161,63,1)"},
		{"name": "Банер литий 1.6м (надійшло)", "data": baner_lyt_by_months_data_16_in, "pointPadding": 0.42, "pointPlacement": -0.2, "color": "rgba(186,60,61,.9)"},

		{"name": "Банер литий 2.2м (використано)", "data": baner_lyt_by_months_data_22, "pointPadding": 0.36, "pointPlacement": 0.0, "color": "rgba(171,168,169,1)"},
		{"name": "Банер литий 2.2м (надійшло)", "data": baner_lyt_by_months_data_22_in, "pointPadding": 0.42, "pointPlacement": 0.0, "color": "rgba(73,70,70,.9)"},
		
		{"name": "Банер литий 2.5м (використано)", "data": baner_lyt_by_months_data_25, "pointPadding": 0.36, "pointPlacement": 0.2, "color": "rgba(138,255,174,1)"},
		{"name": "Банер литий 2.5м (надійшло)", "data": baner_lyt_by_months_data_25_in, "pointPadding": 0.42, "pointPlacement": 0.2, "color": "rgba(29,130,60,.9)"},

		{"name": "Банер литий 3.2м (використано)", "data": baner_lyt_by_months_data_32, "pointPadding": 0.36, "pointPlacement": 0.4, "color": "rgba(138,255,174,1)"},
		{"name": "Банер литий 3.2м (надійшло)", "data": baner_lyt_by_months_data_32_in, "pointPadding": 0.42, "pointPlacement": 0.4, "color": "rgba(29,130,60,.9)"},
]

	# print(all_baner_by_months_data)

	#End filtering by months ####################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	charts_data_baner_lyt_months = json.dumps(all_baner_by_months_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_baner_lyt.html', locals())

def printstatistics_baner_sitka(request):
		
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

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_baner_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_baner_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	baner_sitka_by_months_22 = dict()
	baner_sitka_by_months_25 = dict()
	baner_sitka_by_months_32 = dict()

	baner_sitka_by_months_22_in = dict()
	baner_sitka_by_months_25_in = dict()
	baner_sitka_by_months_32_in = dict()

	for order_by_months in all_baner_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 23:
			if order_by_months["date_item"] in baner_sitka_by_months_22:
				baner_sitka_by_months_22[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_sitka_by_months_22[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 24:
			if order_by_months["date_item"] in baner_sitka_by_months_25:
				baner_sitka_by_months_25[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_sitka_by_months_25[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 8:
			if order_by_months["date_item"] in baner_sitka_by_months_32:
				baner_sitka_by_months_32[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				baner_sitka_by_months_32[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_baner_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 29:
			if order_by_months_in["date_item"] in baner_sitka_by_months_22_in:
				baner_sitka_by_months_22_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_sitka_by_months_22_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 16:
			if order_by_months_in["date_item"] in baner_sitka_by_months_25_in:
				baner_sitka_by_months_25_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_sitka_by_months_25_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 15:
			if order_by_months_in["date_item"] in baner_sitka_by_months_32_in:
				baner_sitka_by_months_32_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				baner_sitka_by_months_32_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]


	baner_sitka_by_months_data_22 = list()
	for month_item in months_list:
		if month_item in baner_sitka_by_months_22:
			baner_sitka_by_months_data_22.append(baner_sitka_by_months_22[month_item])
		else:
			baner_sitka_by_months_data_22.append(0)

	baner_sitka_by_months_data_25 = list()
	for month_item in months_list:
		if month_item in baner_sitka_by_months_25:
			baner_sitka_by_months_data_25.append(baner_sitka_by_months_25[month_item])
		else:
			baner_sitka_by_months_data_25.append(0)

	baner_sitka_by_months_data_32 = list()
	for month_item in months_list:
		if month_item in baner_sitka_by_months_32:
			baner_sitka_by_months_data_32.append(baner_sitka_by_months_32[month_item])
		else:
			baner_sitka_by_months_data_32.append(0)


	baner_sitka_by_months_data_22_in = list()
	for month_item in months_list:
		if month_item in baner_sitka_by_months_22_in:
			baner_sitka_by_months_data_22_in.append(baner_sitka_by_months_22_in[month_item])
		else:
			baner_sitka_by_months_data_22_in.append(0)

	baner_sitka_by_months_data_25_in = list()
	for month_item in months_list:
		if month_item in baner_sitka_by_months_25_in:
			baner_sitka_by_months_data_25_in.append(baner_sitka_by_months_25_in[month_item])
		else:
			baner_sitka_by_months_data_25_in.append(0)

	baner_sitka_by_months_data_32_in = list()
	for month_item in months_list:
		if month_item in baner_sitka_by_months_32_in:
			baner_sitka_by_months_data_32_in.append(baner_sitka_by_months_32_in[month_item])
		else:
			baner_sitka_by_months_data_32_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_baner_by_months_data = dict()
	all_baner_by_months_data["chart_print"] = dict()
	all_baner_by_months_data["chart_print"]["months_list"] = months_list
	all_baner_by_months_data["chart_print"]["months_series"] = [

		{"name": "Банерна сітка 2.2м (використано)", "data": baner_sitka_by_months_data_22, "pointPadding": 0.3, "pointPlacement": -0.3, "color": "rgba(165,170,217,1)"},
		{"name": "Банерна сітка 2.2м (надійшло)", "data": baner_sitka_by_months_data_22_in, "pointPadding": 0.4, "pointPlacement": -0.3, "color": "rgba(126,86,134,.9)"},

		{"name": "Банерна сітка 2.5м (використано)", "data": baner_sitka_by_months_data_25, "pointPadding": 0.3, "pointPlacement": 0.0, "color": "rgba(248,161,63,1)"},
		{"name": "Банерна сітка 2.5м (надійшло)", "data": baner_sitka_by_months_data_25_in, "pointPadding": 0.4, "pointPlacement": 0.0, "color": "rgba(186,60,61,.9)"},

		{"name": "Банерна сітка 3.2м (використано)", "data": baner_sitka_by_months_data_32, "pointPadding": 0.3, "pointPlacement": 0.3, "color": "rgba(171,168,169,1)"},
		{"name": "Банерна сітка 3.2м (надійшло)", "data": baner_sitka_by_months_data_32_in, "pointPadding": 0.4, "pointPlacement": 0.3, "color": "rgba(73,70,70,.9)"},

	]
	# print(all_baner_by_months_data)

	#End filtering by months ####################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	charts_data_baner_sitka_months = json.dumps(all_baner_by_months_data, default=custom_serializer)

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

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_baner_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_baner_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	beklit_by_months_22 = dict()
	beklit_by_months_25 = dict()
	beklit_by_months_32 = dict()

	beklit_by_months_22_in = dict()
	beklit_by_months_25_in = dict()
	beklit_by_months_32_in = dict()

	for order_by_months in all_baner_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 18:
			if order_by_months["date_item"] in beklit_by_months_22:
				beklit_by_months_22[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				beklit_by_months_22[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 17:
			if order_by_months["date_item"] in beklit_by_months_25:
				beklit_by_months_25[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				beklit_by_months_25[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 5:
			if order_by_months["date_item"] in beklit_by_months_32:
				beklit_by_months_32[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				beklit_by_months_32[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_baner_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 10:
			if order_by_months_in["date_item"] in beklit_by_months_22_in:
				beklit_by_months_22_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				beklit_by_months_22_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 9:
			if order_by_months_in["date_item"] in beklit_by_months_25_in:
				beklit_by_months_25_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				beklit_by_months_25_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 8:
			if order_by_months_in["date_item"] in beklit_by_months_32_in:
				beklit_by_months_32_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				beklit_by_months_32_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	# print(beklit_by_months_22)
	# print(beklit_by_months_25)
	# print(beklit_by_months_32)
	# print(beklit_by_months_22_in)
	# print(beklit_by_months_25_in)
	# print(beklit_by_months_32_in)

	beklit_by_months_data_22 = list()
	for month_item in months_list:
		if month_item in beklit_by_months_22:
			beklit_by_months_data_22.append(beklit_by_months_22[month_item])
		else:
			beklit_by_months_data_22.append(0)

	beklit_by_months_data_25 = list()
	for month_item in months_list:
		if month_item in beklit_by_months_25:
			beklit_by_months_data_25.append(beklit_by_months_25[month_item])
		else:
			beklit_by_months_data_25.append(0)

	beklit_by_months_data_32 = list()
	for month_item in months_list:
		if month_item in beklit_by_months_32:
			beklit_by_months_data_32.append(beklit_by_months_32[month_item])
		else:
			beklit_by_months_data_32.append(0)


	beklit_by_months_data_22_in = list()
	for month_item in months_list:
		if month_item in beklit_by_months_22_in:
			beklit_by_months_data_22_in.append(beklit_by_months_22_in[month_item])
		else:
			beklit_by_months_data_22_in.append(0)

	beklit_by_months_data_25_in = list()
	for month_item in months_list:
		if month_item in beklit_by_months_25_in:
			beklit_by_months_data_25_in.append(beklit_by_months_25_in[month_item])
		else:
			beklit_by_months_data_25_in.append(0)

	beklit_by_months_data_32_in = list()
	for month_item in months_list:
		if month_item in beklit_by_months_32_in:
			beklit_by_months_data_32_in.append(beklit_by_months_32_in[month_item])
		else:
			beklit_by_months_data_32_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_baner_by_months_data = dict()
	all_baner_by_months_data["chart_print"] = dict()
	all_baner_by_months_data["chart_print"]["months_list"] = months_list
	all_baner_by_months_data["chart_print"]["months_series"] = [

		{"name": "Бекліт 2.2м (використано)", "data": beklit_by_months_data_22, "pointPadding": 0.3, "pointPlacement": -0.3, "color": "rgba(165,170,217,1)"},
		{"name": "Бекліт 2.2м (надійшло)", "data": beklit_by_months_data_22_in, "pointPadding": 0.4, "pointPlacement": -0.3, "color": "rgba(126,86,134,.9)"},

		{"name": "Бекліт 2.5м (використано)", "data": beklit_by_months_data_25, "pointPadding": 0.3, "pointPlacement": 0.0, "color": "rgba(248,161,63,1)"},
		{"name": "Бекліт 2.5м (надійшло)", "data": beklit_by_months_data_25_in, "pointPadding": 0.4, "pointPlacement": 0.0, "color": "rgba(186,60,61,.9)"},

		{"name": "Бекліт 3.2м (використано)", "data": beklit_by_months_data_32, "pointPadding": 0.3, "pointPlacement": 0.3, "color": "rgba(171,168,169,1)"},
		{"name": "Бекліт 3.2м (надійшло)", "data": beklit_by_months_data_32_in, "pointPadding": 0.4, "pointPlacement": 0.3, "color": "rgba(73,70,70,.9)"},

	]
	# print(all_baner_by_months_data)
	#end of filtering by months##############################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_baner = json.dumps(all_baner_by_days_data, default=custom_serializer)

	charts_data_beklit_months = json.dumps(all_baner_by_months_data, default=custom_serializer)

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
	orah_by_days_105 = dict()

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

		if order_by_days["material_id"] == 40:
			if order_by_days["date_item"] in orah_by_days_105:
				orah_by_days_105[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				orah_by_days_105[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

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

	orah_by_days_105_data = list()
	for day_item in days_list:
		if day_item in orah_by_days_105:
			orah_by_days_105_data.append(orah_by_days_105[day_item])
		else:
			orah_by_days_105_data.append(0)

	all_oracal_by_days_data = dict()
	all_oracal_by_days_data["chart_print"] = dict()
	all_oracal_by_days_data["chart_print"]["days_list"] = days_list
	all_oracal_by_days_data["chart_print"]["series"] = [
		{"name": "Оракал глянцевий прозорий 1,37м", "data": orah_by_days_1_data},
		{"name": "Оракал глянцевий білий 1,05м", "data": orah_by_days_105_data},
		{"name": "Оракал глянцевий прозорий 1,05м", "data": orah_by_days_126_data},
		{"name": "Оракал глянцевий білий 1,37м", "data": orah_by_days_137_data},
	]

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_orah_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_orah_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	orah_by_months_1 = dict()
	orah_by_months_105 = dict()
	orah_by_months_126 = dict()
	orah_by_months_137 = dict()

	orah_by_months_1_in = dict()
	orah_by_months_105_in = dict()
	orah_by_months_126_in = dict()
	orah_by_months_137_in = dict()

	for order_by_months in all_orah_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 27:
			if order_by_months["date_item"] in orah_by_months_1:
				orah_by_months_1[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				orah_by_months_1[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 40:
			if order_by_months["date_item"] in orah_by_months_105:
				orah_by_months_105[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				orah_by_months_105[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 31:
			if order_by_months["date_item"] in orah_by_months_126:
				orah_by_months_126[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				orah_by_months_126[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 6:
			if order_by_months["date_item"] in orah_by_months_137:
				orah_by_months_137[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				orah_by_months_137[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_orah_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 21:
			if order_by_months_in["date_item"] in orah_by_months_1_in:
				orah_by_months_1_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				orah_by_months_1_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 41:
			if order_by_months_in["date_item"] in orah_by_months_105_in:
				orah_by_months_105_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				orah_by_months_105_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 32:
			if order_by_months_in["date_item"] in orah_by_months_126_in:
				orah_by_months_126_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				orah_by_months_126_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 19:
			if order_by_months_in["date_item"] in orah_by_months_137_in:
				orah_by_months_137_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				orah_by_months_137_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	# print(orah_by_months_1)
	# print(orah_by_months_126)
	# print(orah_by_months_137)
	# print(orah_by_months_1_in)
	# print(orah_by_months_126_in)
	# print(orah_by_months_137_in)

	orah_by_months_data_1 = list()
	for month_item in months_list:
		if month_item in orah_by_months_1:
			orah_by_months_data_1.append(orah_by_months_1[month_item])
		else:
			orah_by_months_data_1.append(0)

	orah_by_months_data_105 = list()
	for month_item in months_list:
		if month_item in orah_by_months_105:
			orah_by_months_data_105.append(orah_by_months_105[month_item])
		else:
			orah_by_months_data_105.append(0)

	orah_by_months_data_126 = list()
	for month_item in months_list:
		if month_item in orah_by_months_126:
			orah_by_months_data_126.append(orah_by_months_126[month_item])
		else:
			orah_by_months_data_126.append(0)

	orah_by_months_data_137 = list()
	for month_item in months_list:
		if month_item in orah_by_months_137:
			orah_by_months_data_137.append(orah_by_months_137[month_item])
		else:
			orah_by_months_data_137.append(0)


	orah_by_months_data_1_in = list()
	for month_item in months_list:
		if month_item in orah_by_months_1_in:
			orah_by_months_data_1_in.append(orah_by_months_1_in[month_item])
		else:
			orah_by_months_data_1_in.append(0)
			
	orah_by_months_data_105_in = list()
	for month_item in months_list:
		if month_item in orah_by_months_105_in:
			orah_by_months_data_105_in.append(orah_by_months_105_in[month_item])
		else:
			orah_by_months_data_105_in.append(0)

	orah_by_months_data_126_in = list()
	for month_item in months_list:
		if month_item in orah_by_months_126_in:
			orah_by_months_data_126_in.append(orah_by_months_126_in[month_item])
		else:
			orah_by_months_data_126_in.append(0)

	orah_by_months_data_137_in = list()
	for month_item in months_list:
		if month_item in orah_by_months_137_in:
			orah_by_months_data_137_in.append(orah_by_months_137_in[month_item])
		else:
			orah_by_months_data_137_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_orah_by_months_data = dict()
	all_orah_by_months_data["chart_print"] = dict()
	all_orah_by_months_data["chart_print"]["months_list"] = months_list
	all_orah_by_months_data["chart_print"]["months_series"] = [

		{"name": "Оракал глянцевий прозорий 1,37м (використано)", "data": orah_by_months_data_1, "pointPadding": 0.35, "pointPlacement": -0.35, "color": "rgba(165,170,217,1)"},
		{"name": "Оракал глянцевий прозорий 1,37м (надійшло)", "data": orah_by_months_data_1_in, "pointPadding": 0.42, "pointPlacement": -0.35, "color": "rgba(126,86,134,.9)"},

		{"name": "Оракал глянцевий білий 1,05м (використано)", "data": orah_by_months_data_105, "pointPadding": 0.35, "pointPlacement": -0.12, "color": "rgba(248,161,63,1)"},
		{"name": "Оракал глянцевий білий 1,05м (надійшло)", "data": orah_by_months_data_105_in, "pointPadding": 0.42, "pointPlacement": -0.12, "color": "rgba(186,60,61,.9)"},

		{"name": "Оракал глянцевий прозорий 1,05м (використано)", "data": orah_by_months_data_126, "pointPadding": 0.35, "pointPlacement": 0.12, "color": "rgba(171,168,169,1)"},
		{"name": "Оракал глянцевий прозорий 1,05м (надійшло)", "data": orah_by_months_data_126_in, "pointPadding": 0.42, "pointPlacement": 0.12, "color": "rgba(73,70,70,.9)"},

		{"name": "Оракал глянцевий білий 1,37м (використано)", "data": orah_by_months_data_137, "pointPadding": 0.35, "pointPlacement": 0.35, "color": "rgba(138,255,174,1)"},
		{"name": "Оракал глянцевий білий 1,37м (надійшло)", "data": orah_by_months_data_137_in, "pointPadding": 0.42, "pointPlacement": 0.35, "color": "rgba(29,130,60,.9)"},

	]
	# print(all_orah_by_months_data)
	#end of filtering by months##############################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_oracal = json.dumps(all_oracal_by_days_data, default=custom_serializer)

	charts_data_oracal_months = json.dumps(all_orah_by_months_data, default=custom_serializer)

	# print (charts_data_oracal_months)

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
	oram_by_days_105 = dict()

	for order_by_days in all_oracal_by_days:
		if not order_by_days["date_item"] in days_list:
			days_list.append(order_by_days["date_item"])

		if order_by_days["material_id"] == 28:
			if order_by_days["date_item"] in oram_by_days_1:
				oram_by_days_1[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				oram_by_days_1[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 41:
			if order_by_days["date_item"] in oram_by_days_105:
				oram_by_days_105[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				oram_by_days_105[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

		if order_by_days["material_id"] == 34:
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

	oram_by_days_105_data = list()
	for day_item in days_list:
		if day_item in oram_by_days_105:
			oram_by_days_105_data.append(oram_by_days_105[day_item])
		else:
			oram_by_days_105_data.append(0)

	all_oracal_by_days_data = dict()
	all_oracal_by_days_data["chart_print"] = dict()
	all_oracal_by_days_data["chart_print"]["days_list"] = days_list
	all_oracal_by_days_data["chart_print"]["series"] = [
		{"name": "Оракал матовий прозорий 1,37м", "data": oram_by_days_1_data},
		{"name": "Оракал матовий білий 1,05м", "data": oram_by_days_105_data},
		{"name": "Оракал матовий прозорий 1,05м", "data": oram_by_days_126_data},
		{"name": "Оракал матовий білий 1,37м", "data": oram_by_days_137_data},
	]

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_oram_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_oram_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	oram_by_months_1 = dict()
	oram_by_months_105 = dict()
	oram_by_months_126 = dict()
	oram_by_months_137 = dict()

	oram_by_months_1_in = dict()
	oram_by_months_105_in = dict()
	oram_by_months_126_in = dict()
	oram_by_months_137_in = dict()

	for order_by_months in all_oram_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 28:
			if order_by_months["date_item"] in oram_by_months_1:
				oram_by_months_1[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				oram_by_months_1[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 41:
			if order_by_months["date_item"] in oram_by_months_105:
				oram_by_months_105[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				oram_by_months_105[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 34:
			if order_by_months["date_item"] in oram_by_months_126:
				oram_by_months_126[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				oram_by_months_126[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 7:
			if order_by_months["date_item"] in oram_by_months_137:
				oram_by_months_137[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				oram_by_months_137[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_oram_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 22:
			if order_by_months_in["date_item"] in oram_by_months_1_in:
				oram_by_months_1_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				oram_by_months_1_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 42:
			if order_by_months_in["date_item"] in oram_by_months_105_in:
				oram_by_months_105_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				oram_by_months_105_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 34:
			if order_by_months_in["date_item"] in oram_by_months_126_in:
				oram_by_months_126_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				oram_by_months_126_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 20:
			if order_by_months_in["date_item"] in oram_by_months_137_in:
				oram_by_months_137_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				oram_by_months_137_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	# print(orah_by_months_1)
	# print(orah_by_months_126)
	# print(orah_by_months_137)
	# print(orah_by_months_1_in)
	# print(orah_by_months_126_in)
	# print(orah_by_months_137_in)

	oram_by_months_data_1 = list()
	for month_item in months_list:
		if month_item in oram_by_months_1:
			oram_by_months_data_1.append(oram_by_months_1[month_item])
		else:
			oram_by_months_data_1.append(0)

	oram_by_months_data_105 = list()
	for month_item in months_list:
		if month_item in oram_by_months_105:
			oram_by_months_data_105.append(oram_by_months_105[month_item])
		else:
			oram_by_months_data_105.append(0)

	oram_by_months_data_126 = list()
	for month_item in months_list:
		if month_item in oram_by_months_126:
			oram_by_months_data_126.append(oram_by_months_126[month_item])
		else:
			oram_by_months_data_126.append(0)

	oram_by_months_data_137 = list()
	for month_item in months_list:
		if month_item in oram_by_months_137:
			oram_by_months_data_137.append(oram_by_months_137[month_item])
		else:
			oram_by_months_data_137.append(0)


	oram_by_months_data_1_in = list()
	for month_item in months_list:
		if month_item in oram_by_months_1_in:
			oram_by_months_data_1_in.append(oram_by_months_1_in[month_item])
		else:
			oram_by_months_data_1_in.append(0)
			
	oram_by_months_data_105_in = list()
	for month_item in months_list:
		if month_item in oram_by_months_105_in:
			oram_by_months_data_105_in.append(oram_by_months_105_in[month_item])
		else:
			oram_by_months_data_105_in.append(0)

	oram_by_months_data_126_in = list()
	for month_item in months_list:
		if month_item in oram_by_months_126_in:
			oram_by_months_data_126_in.append(oram_by_months_126_in[month_item])
		else:
			oram_by_months_data_126_in.append(0)

	oram_by_months_data_137_in = list()
	for month_item in months_list:
		if month_item in oram_by_months_137_in:
			oram_by_months_data_137_in.append(oram_by_months_137_in[month_item])
		else:
			oram_by_months_data_137_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_oram_by_months_data = dict()
	all_oram_by_months_data["chart_print"] = dict()
	all_oram_by_months_data["chart_print"]["months_list"] = months_list
	all_oram_by_months_data["chart_print"]["months_series"] = [

		{"name": "Оракал матовий прозорий 1.37м (використано)", "data": oram_by_months_data_1, "pointPadding": 0.35, "pointPlacement": -0.35, "color": "rgba(165,170,217,1)"},
		{"name": "Оракал матовий прозорий 1.37м (надійшло)", "data": oram_by_months_data_1_in, "pointPadding": 0.42, "pointPlacement": -0.35, "color": "rgba(126,86,134,.9)"},

		{"name": "Оракал матовий білий 1.05м (використано)", "data": oram_by_months_data_105, "pointPadding": 0.35, "pointPlacement": -0.12, "color": "rgba(248,161,63,1)"},
		{"name": "Оракал матовий білий 1.05м (надійшло)", "data": oram_by_months_data_105_in, "pointPadding": 0.42, "pointPlacement": -0.12, "color": "rgba(186,60,61,.9)"},

		{"name": "Оракал матовий прозорий 1.05м (використано)", "data": oram_by_months_data_126, "pointPadding": 0.35, "pointPlacement": 0.12, "color": "rgba(171,168,169,1)"},
		{"name": "Оракал матовий прозорий 1.05м (надійшло)", "data": oram_by_months_data_126_in, "pointPadding": 0.42, "pointPlacement": 0.12, "color": "rgba(73,70,70,.9)"},

		{"name": "Оракал матовий білий 1.37м (використано)", "data": oram_by_months_data_137, "pointPadding": 0.35, "pointPlacement": 0.35, "color": "rgba(138,255,174,1)"},
		{"name": "Оракал матовий білий 1.37м (надійшло)", "data": oram_by_months_data_137_in, "pointPadding": 0.42, "pointPlacement": 0.35, "color": "rgba(29,130,60,.9)"},

	]
	# print(all_baner_by_months_data)
	#end of filtering by months##############################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_oracal = json.dumps(all_oracal_by_days_data, default=custom_serializer)
	charts_data_oracal_months = json.dumps(all_oram_by_months_data, default=custom_serializer)

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

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_scroll_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_scroll_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	scroll_by_months_127 = dict()
	scroll_by_months_315 = dict()

	scroll_by_months_127_in = dict()
	scroll_by_months_315_in = dict()

	for order_by_months in all_scroll_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 14:
			if order_by_months["date_item"] in scroll_by_months_127:
				scroll_by_months_127[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				scroll_by_months_127[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 9:
			if order_by_months["date_item"] in scroll_by_months_315:
				scroll_by_months_315[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				scroll_by_months_315[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_scroll_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 4:
			if order_by_months_in["date_item"] in scroll_by_months_127_in:
				scroll_by_months_127_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				scroll_by_months_127_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 3:
			if order_by_months_in["date_item"] in scroll_by_months_315_in:
				scroll_by_months_315_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				scroll_by_months_315_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	scroll_by_months_data_127 = list()
	for month_item in months_list:
		if month_item in scroll_by_months_127:
			scroll_by_months_data_127.append(scroll_by_months_127[month_item])
		else:
			scroll_by_months_data_127.append(0)

	scroll_by_months_data_315 = list()
	for month_item in months_list:
		if month_item in scroll_by_months_315:
			scroll_by_months_data_315.append(scroll_by_months_315[month_item])
		else:
			scroll_by_months_data_315.append(0)


	scroll_by_months_data_127_in = list()
	for month_item in months_list:
		if month_item in scroll_by_months_127_in:
			scroll_by_months_data_127_in.append(scroll_by_months_127_in[month_item])
		else:
			scroll_by_months_data_127_in.append(0)

	scroll_by_months_data_315_in = list()
	for month_item in months_list:
		if month_item in scroll_by_months_315_in:
			scroll_by_months_data_315_in.append(scroll_by_months_315_in[month_item])
		else:
			scroll_by_months_data_315_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_scroll_by_months_data = dict()
	all_scroll_by_months_data["chart_print"] = dict()
	all_scroll_by_months_data["chart_print"]["months_list"] = months_list
	all_scroll_by_months_data["chart_print"]["months_series"] = [

		{"name": "Скролл 1.27м (використано)", "data": scroll_by_months_data_127, "pointPadding": 0.3, "pointPlacement": -0.2, "color": "rgba(165,170,217,1)"},
		{"name": "Скролл 1.27м (надійшло)", "data": scroll_by_months_data_127_in, "pointPadding": 0.4, "pointPlacement": -0.2, "color": "rgba(126,86,134,.9)"},

		{"name": "Скролл 3.15м (використано)", "data": scroll_by_months_data_315, "pointPadding": 0.3, "pointPlacement": 0.2, "color": "rgba(248,161,63,1)"},
		{"name": "Скролл 3.15м (надійшло)", "data": scroll_by_months_data_315_in, "pointPadding": 0.4, "pointPlacement": 0.2, "color": "rgba(186,60,61,.9)"},

	]

	# print(all_baner_by_months_data)
	#end of filtering by months##############################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_scroll = json.dumps(all_scroll_by_days_data, default=custom_serializer)

	charts_data_scroll_months = json.dumps(all_scroll_by_months_data, default=custom_serializer)

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
	sitik_by_days_129 = dict()
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

		if order_by_days["material_id"] == 33:
			if order_by_days["date_item"] in sitik_by_days_129:
				sitik_by_days_129[order_by_days["date_item"]] += order_by_days["m_kv_amount"]
			else:
				sitik_by_days_129[order_by_days["date_item"]] = order_by_days["m_kv_amount"]

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

	sitik_by_days_data_129 = list()
	for day_item in days_list:
		if day_item in sitik_by_days_129:
			sitik_by_days_data_129.append(sitik_by_days_129[day_item])
		else:
			sitik_by_days_data_129.append(0)

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
		{"name": "Сітік 1.29м", "data": sitik_by_days_data_129},
		{"name": "Сітік 1.6м", "data": sitik_by_days_data_16},
	]

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_sitik_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_sitik_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	sitik_by_months_125 = dict()
	sitik_by_months_127 = dict()
	sitik_by_months_129 = dict()
	sitik_by_months_16 = dict()

	sitik_by_months_125_in = dict()
	sitik_by_months_127_in = dict()
	sitik_by_months_129_in = dict()
	sitik_by_months_16_in = dict()

	for order_by_months in all_sitik_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 25:
			if order_by_months["date_item"] in sitik_by_months_125:
				sitik_by_months_125[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				sitik_by_months_125[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 2:
			if order_by_months["date_item"] in sitik_by_months_127:
				sitik_by_months_127[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				sitik_by_months_127[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 33:
			if order_by_months["date_item"] in sitik_by_months_129:
				sitik_by_months_129[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				sitik_by_months_129[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 26:
			if order_by_months["date_item"] in sitik_by_months_16:
				sitik_by_months_16[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				sitik_by_months_16[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_sitik_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 27:
			if order_by_months_in["date_item"] in sitik_by_months_125_in:
				sitik_by_months_125_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				sitik_by_months_125_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 17:
			if order_by_months_in["date_item"] in sitik_by_months_127_in:
				sitik_by_months_127_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				sitik_by_months_127_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 33:
			if order_by_months_in["date_item"] in sitik_by_months_129_in:
				sitik_by_months_129_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				sitik_by_months_129_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 18:
			if order_by_months_in["date_item"] in sitik_by_months_16_in:
				sitik_by_months_16_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				sitik_by_months_16_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]


	sitik_by_months_data_125 = list()
	for month_item in months_list:
		if month_item in sitik_by_months_125:
			sitik_by_months_data_125.append(sitik_by_months_125[month_item])
		else:
			sitik_by_months_data_125.append(0)

	sitik_by_months_data_127 = list()
	for month_item in months_list:
		if month_item in sitik_by_months_127:
			sitik_by_months_data_127.append(sitik_by_months_127[month_item])
		else:
			sitik_by_months_data_127.append(0)

	sitik_by_months_data_129 = list()
	for month_item in months_list:
		if month_item in sitik_by_months_129:
			sitik_by_months_data_129.append(sitik_by_months_129[month_item])
		else:
			sitik_by_months_data_129.append(0)

	sitik_by_months_data_16 = list()
	for month_item in months_list:
		if month_item in sitik_by_months_16:
			sitik_by_months_data_16.append(sitik_by_months_16[month_item])
		else:
			sitik_by_months_data_16.append(0)



	sitik_by_months_data_125_in = list()
	for month_item in months_list:
		if month_item in sitik_by_months_125_in:
			sitik_by_months_data_125_in.append(sitik_by_months_125_in[month_item])
		else:
			sitik_by_months_data_125_in.append(0)

	sitik_by_months_data_127_in = list()
	for month_item in months_list:
		if month_item in sitik_by_months_127_in:
			sitik_by_months_data_127_in.append(sitik_by_months_127_in[month_item])
		else:
			sitik_by_months_data_127_in.append(0)

	sitik_by_months_data_129_in = list()
	for month_item in months_list:
		if month_item in sitik_by_months_129_in:
			sitik_by_months_data_129_in.append(sitik_by_months_129_in[month_item])
		else:
			sitik_by_months_data_129_in.append(0)

	sitik_by_months_data_16_in = list()
	for month_item in months_list:
		if month_item in sitik_by_months_16_in:
			sitik_by_months_data_16_in.append(sitik_by_months_16_in[month_item])
		else:
			sitik_by_months_data_16_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_sitik_by_months_data = dict()
	all_sitik_by_months_data["chart_print"] = dict()
	all_sitik_by_months_data["chart_print"]["months_list"] = months_list
	all_sitik_by_months_data["chart_print"]["months_series"] = [

		{"name": "Сітік 1.25м (використано)", "data": sitik_by_months_data_125, "pointPadding": 0.35, "pointPlacement": -0.35, "color": "rgba(165,170,217,1)"},
		{"name": "Сітік 1.25м (надійшло)", "data": sitik_by_months_data_125_in, "pointPadding": 0.42, "pointPlacement": -0.35, "color": "rgba(126,86,134,.9)"},

		{"name": "Сітік 1.27м (використано)", "data": sitik_by_months_data_127, "pointPadding": 0.35, "pointPlacement": -0.12, "color": "rgba(248,161,63,1)"},
		{"name": "Сітік 1.27м (надійшло)", "data": sitik_by_months_data_127_in, "pointPadding": 0.42, "pointPlacement": -0.12, "color": "rgba(186,60,61,.9)"},

		{"name": "Сітік 1.29м (використано)", "data": sitik_by_months_data_129, "pointPadding": 0.35, "pointPlacement": 0.12, "color": "rgba(171,168,169,1)"},
		{"name": "Сітік 1.29м (надійшло)", "data": sitik_by_months_data_129_in, "pointPadding": 0.42, "pointPlacement": 0.12, "color": "rgba(73,70,70,.9)"},
		
		{"name": "Сітік 1.6м (використано)", "data": sitik_by_months_data_16, "pointPadding": 0.35, "pointPlacement": 0.35, "color": "rgba(138,255,174,1)"},
		{"name": "Сітік 1.6м (надійшло)", "data": sitik_by_months_data_16_in, "pointPadding": 0.42, "pointPlacement": 0.35, "color": "rgba(29,130,60,.9)"},
]

	# print(all_baner_by_months_data)

	#End filtering by months ####################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_sitik = json.dumps(all_sitik_by_days_data, default=custom_serializer)

	charts_data_sitik_months = json.dumps(all_sitik_by_months_data, default=custom_serializer)

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

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_photo_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_photo_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	photos_by_months = dict()
	photop_by_months = dict()

	photos_by_months_in = dict()
	photop_by_months_in = dict()

	for order_by_months in all_photo_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 10:
			if order_by_months["date_item"] in photos_by_months:
				photos_by_months[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				photos_by_months[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 12:
			if order_by_months["date_item"] in photop_by_months:
				photop_by_months[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				photop_by_months[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_photo_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 30:
			if order_by_months_in["date_item"] in photos_by_months_in:
				photos_by_months_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				photos_by_months_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 24:
			if order_by_months_in["date_item"] in photop_by_months_in:
				photop_by_months_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				photop_by_months_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	photos_by_months_data = list()
	for month_item in months_list:
		if month_item in photos_by_months:
			photos_by_months_data.append(photos_by_months[month_item])
		else:
			photos_by_months_data.append(0)

	photop_by_months_data = list()
	for month_item in months_list:
		if month_item in photop_by_months:
			photop_by_months_data.append(photop_by_months[month_item])
		else:
			photop_by_months_data.append(0)


	photos_by_months_data_in = list()
	for month_item in months_list:
		if month_item in photos_by_months_in:
			photos_by_months_data_in.append(photos_by_months_in[month_item])
		else:
			photos_by_months_data_in.append(0)

	photop_by_months_data_in = list()
	for month_item in months_list:
		if month_item in photop_by_months_in:
			photop_by_months_data_in.append(photop_by_months_in[month_item])
		else:
			photop_by_months_data_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_photo_by_months_data = dict()
	all_photo_by_months_data["chart_print"] = dict()
	all_photo_by_months_data["chart_print"]["months_list"] = months_list
	all_photo_by_months_data["chart_print"]["months_series"] = [

		{"name": "Фотопапір 1.07м (використано)", "data": photop_by_months_data, "pointPadding": 0.3, "pointPlacement": -0.2, "color": "rgba(165,170,217,1)"},
		{"name": "Фотопапір 1.07м (надійшло)", "data": photop_by_months_data_in, "pointPadding": 0.4, "pointPlacement": -0.2, "color": "rgba(126,86,134,.9)"},

		{"name": "Фотошпалери (використано)", "data": photos_by_months_data, "pointPadding": 0.3, "pointPlacement": 0.2, "color": "rgba(248,161,63,1)"},
		{"name": "Фотошпалери (надійшло)", "data": photos_by_months_data_in, "pointPadding": 0.4, "pointPlacement": 0.2, "color": "rgba(186,60,61,.9)"},

	]

	# print(all_baner_by_months_data)
	#end of filtering by months##############################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_photo = json.dumps(all_photo_by_days_data, default=custom_serializer)

	charts_data_photo_months = json.dumps(all_photo_by_months_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_photo.html', locals())

def printstatistics_holst(request):
	
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

	#Start filtering by months ##########################################################################################

	today = datetime.datetime.now()
	endmonth = datetime.date.today() + timedelta(days = 1)
	startmonth = endmonth - timedelta(days=365)
	start_curr_year = datetime.datetime(year=today.year, month=1, day=1)

	all_holst_by_months = PrintOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv"))\
		.order_by("date_item")

	all_holst_by_months_in = MaterialOrder.objects.filter(created__range=[start_curr_year, endmonth])\
		.annotate(date_item=ExtractMonth('created'))\
		.values("date_item", "material__name_of_material", "material_id")\
		.annotate(m_kv_amount = Sum("m_kv_of_material"))\
		.order_by("date_item")

	# all_bbs_1 = PrintOrder.objects.filter(created__range=[startmonth, "2018-08-16"], material_id = 1)\
	# 	.annotate(date_item=ExtractMonth('created'))\
	# 	.values("date_item", "material__name_of_material", "material_id")\
	# 	.annotate(m_kv_amount = Sum("m_kv"))\
	# 	.order_by("date_item")

	# print(all_bbs_1)

	# print (all_baner_by_months_in)

	months_list = list()
	onevision_by_months = dict()
	poliman_by_months = dict()
	holst_by_months = dict()

	onevision_by_months_in = dict()
	poliman_by_months_in = dict()
	holst_by_months_in = dict()

	for order_by_months in all_holst_by_months:
		if not order_by_months["date_item"] in months_list:
			months_list.append(order_by_months["date_item"])

		if order_by_months["material_id"] == 13:
			if order_by_months["date_item"] in onevision_by_months:
				onevision_by_months[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				onevision_by_months[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 30:
			if order_by_months["date_item"] in poliman_by_months:
				poliman_by_months[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				poliman_by_months[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

		if order_by_months["material_id"] == 11:
			if order_by_months["date_item"] in holst_by_months:
				holst_by_months[order_by_months["date_item"]] += order_by_months["m_kv_amount"]
			else:
				holst_by_months[order_by_months["date_item"]] = order_by_months["m_kv_amount"]

	for order_by_months_in in all_holst_by_months_in:
		if not order_by_months_in["date_item"] in months_list:
			months_list.append(order_by_months_in["date_item"])

		if order_by_months_in["material_id"] == 23:
			if order_by_months_in["date_item"] in onevision_by_months_in:
				onevision_by_months_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				onevision_by_months_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 26:
			if order_by_months_in["date_item"] in poliman_by_months_in:
				poliman_by_months_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				poliman_by_months_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

		if order_by_months_in["material_id"] == 31:
			if order_by_months_in["date_item"] in holst_by_months_in:
				holst_by_months_in[order_by_months_in["date_item"]] += order_by_months_in["m_kv_amount"]
			else:
				holst_by_months_in[order_by_months_in["date_item"]] = order_by_months_in["m_kv_amount"]

	# print(beklit_by_months_22)
	# print(beklit_by_months_25)
	# print(beklit_by_months_32)
	# print(beklit_by_months_22_in)
	# print(beklit_by_months_25_in)
	# print(beklit_by_months_32_in)

	onevision_by_months_data = list()
	for month_item in months_list:
		if month_item in onevision_by_months:
			onevision_by_months_data.append(onevision_by_months[month_item])
		else:
			onevision_by_months_data.append(0)

	poliman_by_months_data = list()
	for month_item in months_list:
		if month_item in poliman_by_months:
			poliman_by_months_data.append(poliman_by_months[month_item])
		else:
			poliman_by_months_data.append(0)

	holst_by_months_data = list()
	for month_item in months_list:
		if month_item in holst_by_months:
			holst_by_months_data.append(holst_by_months[month_item])
		else:
			holst_by_months_data.append(0)


	onevision_by_months_data_in = list()
	for month_item in months_list:
		if month_item in onevision_by_months_in:
			onevision_by_months_data_in.append(onevision_by_months_in[month_item])
		else:
			onevision_by_months_data_in.append(0)

	poliman_by_months_data_in = list()
	for month_item in months_list:
		if month_item in poliman_by_months_in:
			poliman_by_months_data_in.append(poliman_by_months_in[month_item])
		else:
			poliman_by_months_data_in.append(0)

	holst_by_months_data_in = list()
	for month_item in months_list:
		if month_item in holst_by_months_in:
			holst_by_months_data_in.append(holst_by_months_in[month_item])
		else:
			holst_by_months_data_in.append(0)

	months = {1:'Січень', 2:'Лютий', 3:'Березень', 4:'Квітень', 5:'Травень', 6:'Червень', 7:'Липень', 8:'Серпень', 9:'Вересень', 10:'Жовтень', 11:'Листопад',12:'Грудень'}
	months_list = [months.get(n, n) for n in months_list]

	all_holst_by_months_data = dict()
	all_holst_by_months_data["chart_print"] = dict()
	all_holst_by_months_data["chart_print"]["months_list"] = months_list
	all_holst_by_months_data["chart_print"]["months_series"] = [

		{"name": "Ван Віжн 1.07м (використано)", "data": onevision_by_months_data, "pointPadding": 0.3, "pointPlacement": -0.3, "color": "rgba(165,170,217,1)"},
		{"name": "Ван Віжн 1.07м (надійшло)", "data": onevision_by_months_data_in, "pointPadding": 0.4, "pointPlacement": -0.3, "color": "rgba(126,86,134,.9)"},

		{"name": "Поліман 1.27м (використано)", "data": poliman_by_months_data, "pointPadding": 0.3, "pointPlacement": 0.0, "color": "rgba(248,161,63,1)"},
		{"name": "Поліман 1.27м (надійшло)", "data": poliman_by_months_data_in, "pointPadding": 0.4, "pointPlacement": 0.0, "color": "rgba(186,60,61,.9)"},

		{"name": "Холст (використано)", "data": holst_by_months_data, "pointPadding": 0.3, "pointPlacement": 0.3, "color": "rgba(171,168,169,1)"},
		{"name": "Холст (надійшло)", "data": holst_by_months_data_in, "pointPadding": 0.4, "pointPlacement": 0.3, "color": "rgba(73,70,70,.9)"},

	]
	# print(all_baner_by_months_data)
	#end of filtering by months##############################################################################################################

	def custom_serializer(obj):
		if isinstance(obj, (datetime.date)):
			serial = obj.isoformat()
			return serial
		elif isinstance(obj, decimal.Decimal):
			return float(obj)

	charts_data_holst = json.dumps(all_holst_by_days_data, default=custom_serializer)

	charts_data_holst_months = json.dumps(all_holst_by_months_data, default=custom_serializer)

	# print (charts_data)

	return render(request, 'printstatistics/printstatistics_holst.html', locals())