from django.shortcuts import render
import requests
# Create your views here.


def home(request):
    """some sweet sweet audio"""
    audio_string = "Don't stop, never give up, hold your head high and reach the top, let the world see what you have got, bring it all back to you"
    return render(request, "app/home.html", {'audio_string': convertToAudio(audio_string)})


def stops(request):
    """fetch all the stops into an array created from json"""
    r = requests.get('https://tfe-opendata.com/api/v1/stops')
    stops_array = r.json()["stops"]
    print(str(len(stops_array)) + " stops found")
    return render(request, "app/stops.html", {'stops_array': stops_array})


def convertToAudio(myString):
    """Converts string to a form which can be read aloud by text-to-speech API"""
    myString.replace (" ", "+")
    return myString