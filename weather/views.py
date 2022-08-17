import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=eb09cf984d37b4612a2d5769c2b52baa'

    errMsg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_count = City.objects.filter(name=new_city).count()
            if existing_count == 0:
                res = requests.get(url.format(new_city)).json()

                if res['cod'] == 200:
                    form.save()
                else:
                    errMsg = 'City does not exist in the world'
            else:
                errMsg = 'City already exists'

        if errMsg:
            message = errMsg
            message_class = 'is_danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'

    print(errMsg)

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        res = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'temperature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'icon': res['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {"weather_data": weather_data, 'form': form, 'message': message, 'message_class': message_class }
    return render(request, 'weather/weather.html', context)

