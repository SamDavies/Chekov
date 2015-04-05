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


##############################
# Main Service Choosing Page #
##############################

def live_locations(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/vehicle_locations')
    live_bus_array = r.json()["vehicles"]
    my_lat = request.GET.get('lat')
    my_lng = request.GET.get('lng')
    nearest_10 = nearest_to_me(live_bus_array, my_lat, my_lng, 20)

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


def nearest_to_me(things, my_lat, my_lng, count):
    """find the x (count) nearest buses to my location"""
    def distance_to_me(bus):
        """the euclidean distance between a bus and my location"""
        distance = math.sqrt((float(my_lat) - float(bus['latitude']))**2 + (float(my_lng) - float(bus['longitude']))**2)
        return distance

    sorted_buses = sorted(things, key=distance_to_me)
    return sorted_buses[:count]


################################
# Current Service Details page #
################################

def choose_route(request):
    """pick the route to read out"""
    return render(request, "app/choose_route.html")


def convert_to_audio(my_string):
    """Converts string to a form which can be read aloud by text-to-speech API"""
    my_string.replace(" ", "+")
    return my_string


def next_stop(request):
    """finds the next stop for the user's bus"""
    """example request: http://127.0.0.1:8000/next_stop/?lat=55.864337&lng=-3.066306&num=2 """
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    bus_id = str(request.GET.get("num"))

    journeys = requests.get('https://tfe-opendata.com/api/v1/journeys/'+bus_id).json()["journeys"]
    api_stops = requests.get('https://tfe-opendata.com/api/v1/stops/').json()["stops"]
    possible_stops = next_stops(journeys, api_stops)
    closest_stop = nearest_to_me(possible_stops, lat, lng, 1)

    return render(request, "app/next_stop.html", {'stops': closest_stop})


def next_stops(journeys, api_stops):
    """find stop for each journey based on the current time"""
    the_stops = []

    for journey in journeys:
        for departure in journey["departures"]:
            if is_after_current_time(departure["time"]):
                stop_id = departure['stop_id']
                s = get_stop(stop_id, api_stops)
                the_stops.append(s)
                break
    return the_stops


def get_stop(stop_id, api_stops):
    """find the stop which has the given id"""
    for stop in api_stops:
        if stop['stop_id'] == stop_id:
            return stop


def is_after_current_time(api_time):
    """compares a time against the current time to check if the bus has passed the stop already"""
    hours, minutes = api_time.split(":")
    expected_bus_time = int(hours) * 60 + int(minutes)
    current_time = datetime.datetime.now().minute + (datetime.datetime.now().hour * 60)
    return expected_bus_time >= current_time




