from django.http import HttpResponse
from django.shortcuts import render
import math
import requests
import datetime
import json
import pytz


#########
# Views #
#########

def speech(request):
    """some sweet sweet audio"""
    # audio_string = "Don't stop, never give up, hold your head high and reach the top, " \
    #                "let the world see what you have got, bring it all back to you"
    # audio_string = "Finally Friday night, Feelin' kinda good, lookin' alright, Gotta get movin', " \
    #                "can't be late, Gotta get groovin', just can't wait. ho!"
    audio_string = "O-oh O-oh! Throw your hands in the air. O-oh O-oh! Like you just don't care. " \
                   "O-oh O-oh! There's a party over here. O-oh O-oh! There's a party over there"
    return render(request, "app/speech.html", {'audio_string': convert_to_audio((audio_string))})


def stops(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/stops')
    stops_array = r.json()["stops"]
    print(str(len(stops_array)) + " stops found")
    return render(request, "app/stops.html", {'stops_array': stops_array})


def home(request):
    return render(request, "app/home.html")


def live_locations(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/vehicle_locations')
    live_bus_array = r.json()["vehicles"]
    my_lat = request.GET.get('lat')
    my_lng = request.GET.get('lng')
    nearest_10 = nearest_to_me(live_bus_array, my_lat, my_lng, 20)

    # find the unique service numbers
    nearest_services = []
    feed_data = []
    for bus in nearest_10:
        feed_data.append(dict(service=bus["service_name"], destination=bus["destination"]))

        if bus["service_name"] not in nearest_services:
            nearest_services.append(bus["service_name"])

    print(str(len(live_bus_array)) + " buses found")
    return render(request, "app/feed.html", {'data_feed': json.dumps(feed_data), 'nearest_services': nearest_services,
                                             'services': nearest_10})


def get_feed_element(request):
    """given the service in the get request find the closest journey both ways"""
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    service = request.GET.get('service')
    destination = request.GET.get('destination')

    journey, stop = get_journey(str(service), str(destination), lat, lng)
    if journey is not None:
        journey['service_number'] = service
        three_stops = get_previous_and_next(stop, journey)
    else:
        three_stops = ""

    return render(request, "app/feed-journey.html", {'three_stops': three_stops})


def get_previous_and_next(stop, journey):
    departures = journey['departures']
    api_stops = requests.get('https://tfe-opendata.com/api/v1/stops/').json()["stops"]
    length = len(departures)
    for i in range(length):
        if departures[i]['stop_id'] == stop['stop_id']:
            if i != 0 and i != length-1:
                return get_above_below(-1, 1, departures, i, api_stops)
            else:
                if i == 0:
                    return get_above_below(0, 1, departures, i, api_stops)
                else:
                    return get_above_below(-1, 0, departures, i, api_stops)


def get_above_below(above, below, departures, index, api_stops):
    three_departures = []
    for j in range(above, below+1):
        d = departures[index+j]
        d['name'] = get_stop(d['stop_id'], api_stops)['name']
        three_departures.append(d)
    return three_departures


def next_stop(request):
    """finds the next stop for the user's bus"""
    """example request: http://127.0.0.1:8000/next_stop/?lat=55.864337&lng=-3.066306&num=2&destination=Gyle Centre"""
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    service = str(request.GET.get("num"))
    destination = request.GET.get("destination")

    journey, nearest_stop = get_journey(service, destination, lat, lng)

    return render(request, "app/tracker.html", {'stops': nearest_stop})


###########
# Helpers #
###########

def update_buttons(request):
    """given the current selected buttons, find the new nearest button and miss out the selected"""
    pass


def nearest_to_me(things, my_lat, my_lng, count):
    """find the x (count) nearest buses to my location"""
    def distance_to_me(bus):
        """the euclidean distance between a bus and my location"""
        distance = math.sqrt((float(my_lat) - float(bus['latitude']))**2 + (float(my_lng) - float(bus['longitude']))**2)
        return distance

    sorted_buses = sorted(things, key=distance_to_me)
    return sorted_buses[:count]


def choose_route(request):
    """pick the route to read out"""
    return render(request, "app/feed.html")


def convert_to_audio(my_string):
    """Converts string to a form which can be read aloud by text-to-speech API"""
    my_string.replace(" ", "+")
    return my_string


def get_journey(service, destination, lat, lng):
    url = 'https://tfe-opendata.com/api/v1/journeys/'+service
    journeys = requests.get(url).json()["journeys"]
    journeys = remove_bad_destinations(journeys, destination)

    api_stops = requests.get('https://tfe-opendata.com/api/v1/stops/').json()["stops"]
    possible_stops, possible_journeys = next_stops(journeys, api_stops)
    nearest_stop = nearest_to_me(possible_stops, lat, lng, 1)

    if len(nearest_stop) != 0:
        journey = get_matching_element(possible_journeys, possible_stops, nearest_stop[0])
        return journey, nearest_stop[0]
    else:
        return None, None


def get_matching_element(array1, array2, element):
    """get the element from array1 who's index in array2 is the element"""
    for x in range(0, len(array1)):
        if array2[x] == element:
            return array1[x]


def remove_bad_destinations(array, good_destination):
    good_array = []
    for x in array:
        if x['destination'] == good_destination:
            good_array.append(x)
    return good_array


def next_stops(journeys, api_stops):
    """find stop for each journey based on the current time"""
    the_stops = []
    the_journeys = []

    for journey in journeys:
        for departure in journey["departures"]:
            if is_after_current_time(departure["time"]):
                stop_id = departure['stop_id']
                s = get_stop(stop_id, api_stops)
                the_stops.append(s)
                the_journeys.append(journey)
                break
    return the_stops, the_journeys


def get_stop(stop_id, api_stops):
    """find the stop which has the given id"""
    for stop in api_stops:
        if stop['stop_id'] == stop_id:
            return stop


def is_after_current_time(api_time):
    """compares a time against the current time to check if the bus has passed the stop already"""
    hours, minutes = api_time.split(":")
    expected_bus_time = int(hours) * 60 + int(minutes)
    utc = pytz.timezone('GMT')
    current_time = datetime.datetime.now(utc).minute + (datetime.datetime.now(utc).hour * 60)
    return expected_bus_time >= current_time




