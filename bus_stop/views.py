from django.shortcuts import render
import math
import requests
# Create your views here.


def speech(request):
    """some sweet sweet audio"""
    # audio_string = "Don't stop, never give up, hold your head high and reach the top, " \
    #                "let the world see what you have got, bring it all back to you"
    # audio_string = "Finally Friday night, Feelin' kinda good, lookin' alright, Gotta get movin', " \
    #                "can't be late, Gotta get groovin', just can't wait. ho!"
    audio_string = "O-oh O-oh! Throw your hands in the air. O-oh O-oh! Like you just don't care. " \
                   "O-oh O-oh! There's a party over here. O-oh O-oh! There's a party over there"
    return render(request, "app/home.html", {'audio_string': convert_to_audio(audio_string)})


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
    print(str(len(live_bus_array)) + " buses found")
    return render(request, "app/live_buses.html", {'live_bus_array': live_bus_array})


def nearest_buses(bus_array, my_lat, my_lng, count):
    """find the x (count) nearest buses to my location"""
    def distance_to_me(bus):
        """the euclidean distance between a bus and my location"""
        distance = math.sqrt((my_lat - int(bus.latitude))**2 + (my_lng - int(bus.longitude))**2)
        return distance

    sorted_buses = sorted(bus_array, key=distance_to_me)
    return sorted_buses[:count]


def choose_route(request):
    """pick the route to read out"""
    return render(request, "app/choose_route.html")


def convert_to_audio(myString):
    """Converts string to a form which can be read aloud by text-to-speech API"""
    myString.replace(" ", "+")
    return myString

# def readNextStop(bus,)