from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from store.models import DATABASE


# Create your views here.
def products_view(request):
    if request.method == 'GET':
        return JsonResponse(DATABASE,
                json_dumps_params={'indent': 4,
                                   'ensure_ascii': False})


def shop_view(request):
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            result_str = f.read()
            return HttpResponse(result_str)
