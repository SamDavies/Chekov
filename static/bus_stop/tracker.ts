/// <reference path="leaflet.d.ts" />

/* Tracker Map */

class TrackerMap {
    
    map: any;
    marker: any;
    
    constructor(mapId: string) {
        var map = L.map(mapId).setView(new L.LatLng(0, 0), 13);
        
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        var marker = L.marker(new L.LatLng(0,0)).addTo(map);
        
        this.map = map;
        this.marker = marker;
    }
    
    setLocation(x: number, y: number) {
        console.log("Updating map to: " + x + " " + y);
        
        this.map.panTo([x, y]);
        
        this.map.removeLayer(this.marker);
        this.marker = L.marker(new L.LatLng(x, y)).addTo(this.map);
        this.marker.bindPopup("<b>You are here!</b>");
    }
    
}

// IIFE - Immediately Invoked Function Expression
(function(yourcode) {

    // The global jQuery object is passed as a parameter
    yourcode(window.jQuery, window, document);

}(function($, window, document) {

    // The $ is now locally scoped

    // Listen for the jQuery ready event on the document
    $(function() {
        console.log('The DOM is ready');
        // The DOM is ready!
    });

    console.log('The DOM may not be ready');

    /////////////////////////////////
    // The rest of code goes here! //
    /////////////////////////////////
    
    var lat: String = '0';
    var lng: String = '0';
    var nextStop: String = $('#result').find("#bus-data").attr('data-stop');
    var trackerMap: TrackerMap = new TrackerMap("tracker-map");

    function getData(service, destination, result) {
        getLocation();
        var dynamicData = {};
        dynamicData["lat"] = lat;
        dynamicData["lng"] = lng;
        dynamicData["service"] = service;
        dynamicData["destination"] = destination;
        dynamicData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        return $.ajax({
            url: "../tracker_data/",
            type: "get",
            data: dynamicData
        });
    }

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(saveLocation);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function saveLocation(position) {
        lat = String(position.coords.latitude);
        lng = String(position.coords.longitude);
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function refresh(){
        var resultDiv = $('#result');
        var panelDiv = resultDiv.find("#bus-data");

        var service = panelDiv.attr('data-service');
        var destination = panelDiv.attr('data-destination');
        var stop = panelDiv.attr('data-stop');
        getData(service, destination, resultDiv).done(function (data) {            
            resultDiv.empty();
            resultDiv.append(data);

            if(nextStop != stop){
                var audio = document.getElementById("stop-audio");
                audio.play();
            }
            
            trackerMap.setLocation(data["lat"], data["lng"]);

            nextStop = stop;
        });
    }

    setInterval(function(){ refresh(); }, 10000);
    var a = document.getElementById("stop-audio");
    a.play();
}));
