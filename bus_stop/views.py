from django.shortcuts import render
import math
import requests
import datetime

# Create your views here.


def speech(request):
    """some sweet sweet audio"""
    # audio_string = "Don't stop, never give up, hold your head high and reach the top, " \
    #                "let the world see what you have got, bring it all back to you"
    # audio_string = "Finally Friday night, Feelin' kinda good, lookin' alright, Gotta get movin', " \
    #                "can't be late, Gotta get groovin', just can't wait. ho!"
    audio_string = "O-oh O-oh! Throw your hands in the air. O-oh O-oh! Like you just don't care. " \
                   "O-oh O-oh! There's a party over here. O-oh O-oh! There's a party over there"
    return render(request, "app/home.html", {'audio_string': convert_to_audio((audio_string))})


def stops(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/stops')
    stops_array = r.json()["stops"]
    print(str(len(stops_array)) + " stops found")
    return render(request, "app/stops.html", {'stops_array': stops_array})


def live_locations(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/vehicle_locations')
    live_bus_array = r.json()["vehicles"]
    my_lat = request.GET.get('lat')
    my_lng = request.GET.get('lng')
    nearest_10 = nearest_buses(live_bus_array, my_lat, my_lng, 20)

    # find the unique service numbers
    nearest_services = []
    for bus in nearest_10:
        if bus["service_name"] not in nearest_services:
            nearest_services.append(bus["service_name"])

    print(str(len(live_bus_array)) + " buses found")
    return render(request, "app/choose_route.html", {'nearest_buses': nearest_10, 'nearest_services': nearest_services})


def find_services(buses):
    """For each bus, concatenate its services"""
    r = requests.get('https://tfe-opendata.com/api/v1/services')
    services = r.json()["services"]
    pass


def nearest_buses(bus_array, my_lat, my_lng, count):
    """find the x (count) nearest buses to my location"""
    def distance_to_me(bus):
        """the euclidean distance between a bus and my location"""
        distance = math.sqrt((float(my_lat) - float(bus['latitude']))**2 + (float(my_lng) - float(bus['longitude']))**2)
        return distance

    sorted_buses = sorted(bus_array, key=distance_to_me)
    return sorted_buses[:count]


def choose_route(request):
    """pick the route to read out"""
    return render(request, "app/choose_route.html")


def convert_to_audio(my_string):
    """Converts string to a form which can be read aloud by text-to-speech API"""
    my_string.replace(" ", "+")
    return my_string

def mingles(request):
    bus_id = 1
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    num = request.GET.get("lng")
    current_time = datetime.datetime.now().minute + (datetime.datetime.now().hour * 60)

    def next_stop_on_(service_number):
        """For each pair of stops decide what stops this time could be between for each service number and return the latest time """
        return

    def convertTime():
        """converts to time object """
        shite_time = '23:55'
        hours, minutes = shite_time.split(":")

        return int(hours) * 60 + int(minutes)

    r = requests.get('https://tfe-opendata.com/api/v1/journeys/2')
    journeys = r.json()["journeys"]


    return render(request, "app/mingles.html", {'journeys': journeys, 'time': current_time})



# def readNextStop(bus,)