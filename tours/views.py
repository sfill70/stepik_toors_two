from django.shortcuts import render
from logging import getLogger
from django.views.generic import View
from tours import data
from django.http import HttpResponseNotFound
import random
import plural_ru

_logger = getLogger(__name__)


def custom_handler404(request, _=None):
    return HttpResponseNotFound('Ой, что то сломалось... !')


def get_town(departure):
    town = {'msk': "Москвы", 'spb': "Питера", 'kazan': "Казани", 'nsk': "Новосибирска", 'ekb': "Екатеринбурга"}
    return town.get(departure)


class MainView(View):

    def get(self, request, *args, **kwargs):
        tours = {i: data.tours[i] for i in
                 random.sample(range(1, len(data.tours)), 6)}
        context = {
            'tours': tours,}
        return render(request, 'index.html', context)


class DepartureView(View):

    def get(self, request, departure, *args, **kwargs):
        set_departure = {value.get('departure') for (key, value) in data.tours.items()}
        if departure not in set_departure:
            return custom_handler404(request)

        tours = {key: value for (key, value) in data.tours.items()
                 if value['departure'] == departure}

        town = get_town(departure)
        array_price = []
        array_nights = []

        for keys, value in tours.items():
            array_price.append(value['price'])
            array_nights.append(value['nights'])

        min_price = min(array_price)
        max_price = max(array_price)
        min_nights = min(array_nights)
        max_nights = max(array_nights)
        count_tours = len(array_price)
        min_nights_str = plural_ru.ru(min_nights, ['ночи', 'ночи', 'ночей'])
        max_nights_str = plural_ru.ru(max_nights, ['ночи', 'ночи', 'ночей'])
        context = {
            'tours': tours,
            'town': town,
            'min_price': min_price,
            'max_price': max_price,
            'min_nights': min_nights,
            'max_nights': max_nights,
            'count_tours': count_tours,
            'min_nights_str': min_nights_str,
            'max_nights_str': max_nights_str,
        }

        # надо в setting.py 'level': 'DEBUG' тогда видно переменные
        # _logger.info(array_nights)
        # _logger.info(set_departure)
        return render(request, 'departure.html', context)


class TourView(View):
    def get(self, request, id):
        if id not in data.tours:
            return custom_handler404(request)

        tour = data.tours[id]
        departure = data.tours[id]["departure"]

        town = get_town(departure)

        context = {'tour': tour,
                   'departure': departure,
                   'town': town}
        return render(request, 'tour.html', context)
