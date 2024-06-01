import json
import os
import random

from django.contrib.auth import get_user

from store.models import DATABASE


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False) -> list[dict]:
    """
    Функция фильтрации данных по параметрам

    :param database: База данных. (словарь словарей. В качестве database будет передаваться словарь из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [value for value in database.values() if value['category'] == category_key]
    else:
        result = list(database.values())
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)  # Сортировка по ordering_key и параметру reverse
    return result


def same_category_filter(database: dict[str, dict], product: dict) -> list[dict]:
    """
    Функция фильтрует значения по категории продукта, удаляет из списка сам продукт и перемешивает результат
    :param database: База данных (словарь словарей из models.py).
    :param product: Продукт, по категории которого фильтруются остальные продукты.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    same_category = filtering_category(database, product['category'])
    same_category.remove(product)  # Удаляем лишний товар для показа только оставшихся товаров из категории
    random.shuffle(same_category)
    return same_category


def view_in_cart(request) -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username  # Получаем авторизованного пользователя
    cart = {user: {'products': {}}}  # Создаем пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product in cart['products']:
        cart['products'][id_product] += 1  # Добавляем единицу продукта в корзину
    elif id_product in DATABASE:
        cart['products'][id_product] = 1  # Создаем продукт в корзине
    else:
        return False
    with open('cart.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем корзину
        json.dump(cart_users, f)

    return True


def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product in cart['products']:
        cart['products'].pop(id_product)
    else:
        return False
    with open('cart.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем туда корзину
        json.dump(cart_users, f)

    return True


def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)  # Чтение всей базы корзин

    cart = cart_users.get(username)  # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)
