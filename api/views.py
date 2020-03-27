from django.shortcuts import render
from django.views import View
from forecast.api import get_data, get_next
from .models import Key, Search

def get_ip_address(request):
    """ use requestobject to fetch client machine's IP Address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')    ### Real IP address of client Machine
    return ip 

class Weather(View):
    template_name = 'api/weather.html'
    oc_key = Key.objects.get(site="OC").key
    ds_key = Key.objects.get(site="DS").key

    def get(self, request):
        # Use session to store users location
        if not request.session['location']:
            place = "Belfast"
            request.session['location'] = place
        else:
            place = request.session["location"]

        api_data = get_data(place, self.oc_key, self.ds_key)
        forecast = get_next(api_data, place)
        return render(request, self.template_name, {"hour": forecast[0], "location": place.capitalize(), "town": place.capitalize(), "forecast": forecast[1:4]})

    def post(self, request):
        place = request.POST.get('location')
        request.session['location'] = place # Updating location cookie
        ip = get_ip_address(request) # Obtain IP address
        addSearch = Search.objects.create(location=place, ip=ip).save() # Save search to database
        api_data = get_data(place, self.oc_key, self.ds_key)
        forecast = get_next(api_data, place)
        return render(request, self.template_name, {"hour": forecast[0], "location": place.capitalize(), "town": place.capitalize(), "forecast": forecast[1:4]})