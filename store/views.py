from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from store.models import DATABASE
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart


def products_view(request):
    if request.method == 'GET':
        product_id = request.GET.get('id')
        if product_id:
            if product_id in DATABASE:
                data = DATABASE[product_id]
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            category_key = request.GET.get("category")  # Считали 'category'
            ordered_key = request.GET.get("ordering")  # Если в параметрах есть 'ordering'
            if ordered_key:
                if request.GET.get("reverse") and request.GET.get("reverse").lower() == 'true':  # Если в параметрах
                    # есть 'ordering', есть 'reverse' и 'reverse'=True
                    data = filtering_category(DATABASE, category_key, ordered_key, True)
                else:
                    data = filtering_category(DATABASE, category_key, ordered_key)
            else:
                data = filtering_category(DATABASE, category_key)

        # safe=False позволяет получать в Json любые данные, не только словари
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def shop_view(request):
    if request.method == 'GET':
        return render(request,
                      'store/shop.html',
                      context={"products": DATABASE.values()})


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает с именем html файла
                    with open(f'store/products/{page}.html', encoding='utf-8') as f:
                        return HttpResponse(f.read())
        elif isinstance(page, int):
            if str(page) in DATABASE:
                with open(f'store/products/{DATABASE[str(page)]["html"]}.html', encoding='utf-8') as f:
                    return HttpResponse(f.read())

        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') and request.GET.get('format').lower() == 'json':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]
            product['quantity'] = quantity  # Записываем количество товара в параметры продукта
            product['price_total'] = f"{quantity * product['price_after']:.2f}"  # Общая цена
            products.append(product)
        return render(request, "store/cart.html", context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
