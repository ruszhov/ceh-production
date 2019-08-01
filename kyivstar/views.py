from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import requests

def calls(request):
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
	# print(request.session.session_key)
	# print(request.session.cycle_key)
	return render(request, 'kyivstar/calls.html', locals())

def kyivstar(request):
	# print(request.POST)
	response=''
	if request.method == "POST" and request.is_ajax():
		_from_fe = request.POST['_from']
		_to_fe = request.POST['_to']
		_from = _from_fe+"T00:00:00"
		_to = _to_fe+"T23:59:59"

		url="https://fmc.kyivstar.ua/api/cdr/v1/callstat.json"
		
		querystring = {
	        "token": "eed7f9777c6499f195865273e82a31c061bf0e3370559eab855ec03948924f3c",
	        "from": _from,
	        "to": _to,
	        "names": "on",
	        "departments": "on",
	        "ownership": "on",
	    }
		print(querystring)
		response = requests.request("GET", url, params=querystring)
		print(response)
	else:
		massage = "NO"
	return HttpResponse(response, content_type='application/json')
