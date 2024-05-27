import datetime

from django.http import HttpResponse
from django.shortcuts import render


def datetime_view(request):
    if request.method == 'GET':
        date = datetime.datetime.now()
        return HttpResponse(date.strftime('%H:%M %d/%m/%Y'))
