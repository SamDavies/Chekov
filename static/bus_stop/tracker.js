// IIFE - Immediately Invoked Function Expression
(function (yourcode) {
    // The global jQuery object is passed as a parameter
    yourcode(window.jQuery, window, document);
}(function ($, window, document) {
    // The $ is now locally scoped
    // Listen for the jQuery ready event on the document
    $(function () {
        console.log('The DOM is ready');
        // The DOM is ready!
    });
    console.log('The DOM may not be ready');
    /////////////////////////////////
    // The rest of code goes here! //
    /////////////////////////////////
    var lat = '0';
    var lng = '0';
    var nextStop = $('#result').find("#bus-data").attr('data-stop');
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
        }
        else {
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
    function refresh() {
        var resultDiv = $('#result');
        var panelDiv = resultDiv.find("#bus-data");
        var service = panelDiv.attr('data-service');
        var destination = panelDiv.attr('data-destination');
        var stop = panelDiv.attr('data-stop');
        getData(service, destination, resultDiv).done(function (data) {
            resultDiv.empty();
            resultDiv.append(data);
            if (nextStop != stop) {
                var audio = document.getElementById("stop-audio");
                audio.play();
            }
            nextStop = stop;
        });
    }
    setInterval(function () {
        refresh();
    }, 10000);
    var a = document.getElementById("stop-audio");
    a.play();
}));
//# sourceMappingURL=tracker.js.map