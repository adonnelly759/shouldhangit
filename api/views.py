from django.shortcuts import render, redirect
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

    def get(self, request, location=None):
        if not location:
            # Use session to store users location
            try:
                place = request.session['location']
                ip = get_ip_address(request) # Obtain IP address
                addSearch = Search.objects.create(location=place, ip=ip).save() # Save search to database
            except KeyError:
                place = "Belfast"
        else: 
            place = location
            ip = get_ip_address(request) # Obtain IP address
            addSearch = Search.objects.create(location=place, ip=ip).save() # Save search to database

        request.session['location'] = place # Updating location cookie
        api_data = get_data(place, self.oc_key, self.ds_key)
        forecast = get_next(api_data, place)
        return render(request, self.template_name, {"hour": forecast[0], "location": place.capitalize(), "town": place.capitalize(), "forecast": forecast[1:4]})

    def post(self, request, location=None):
        new_location = request.POST['location']
        ip = get_ip_address(request) # Obtain IP address
        addSearch = Search.objects.create(location=new_location, ip=ip).save() # Save search to database
        return redirect("should:weather", location=new_location)