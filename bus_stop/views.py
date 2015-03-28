from django.shortcuts import render
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


def choose_route(request):
    """pick the route to read out"""
    return render(request, "app/choose_route.html")


def convert_to_audio(myString):
    """Converts string to a form which can be read aloud by text-to-speech API"""
    myString.replace(" ", "+")
    return myString

# def readNextStop(bus,)