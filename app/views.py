from django.shortcuts import render
import requests

# Create your views here.


def stops(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/stops')
    stops_array = r.json()["stops"]
    print(str(len(stops_array)) + " stops found")
    return render(request, "app/stops.html", {'stops_array': stops_array})
