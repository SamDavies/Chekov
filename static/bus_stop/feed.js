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
    var chosenRoute = [];
    var availableDiv = $("#available-routes");
    var chosenDiv = $("#chosen-routes");
    var feedDiv = $("#nearest-buses");
    var lat = '0';
    var lng = '0';
    var indexOf = function (needle) {
        if (typeof Array.prototype.indexOf === 'function') {
            indexOf = Array.prototype.indexOf;
        }
        else {
            indexOf = function (needle) {
                var i = -1, index = -1;
                for (i = 0; i < this.length; i++) {
                    if (this[i] === needle) {
                        index = i;
                        break;
                    }
                }
                return index;
            };
        }
        return indexOf.call(this, needle);
    };
    availableDiv.on("click", "button", function () {
        addButton($(this).text(), chosenDiv, "btn btn-primary");
        $(this).remove();
        refreshElements();
    });
    chosenDiv.on("click", "button", function () {
        addButton($(this).text(), availableDiv, "btn btn-default");
        $(this).remove();
        refreshElements();
    });
    function addButton(button, div, cssClass) {
        var buttonHTML = '<button type="button" class="' + cssClass + '">' + button + '</button> ';
        div.prepend(buttonHTML);
    }
    feedDiv.on("click", ".panel", function () {
        $(this).removeClass("panel-default");
        $(this).addClass("panel-primary");
        var parent = $(this).parent();
        var service = parent.attr('data-service');
        var destination = parent.attr('data-destination');
        window.location.replace("/../tracker/?lat=" + lat + "&lng=" + lng + "&service=" + service + "&destination=" + destination);
    });
    function refreshElements() {
        var buttons = getFilterButtons();
        var feed = $("#nearest-buses").children();
        $.each(feed, function (key, value) {
            var service = $(this).attr('data-service');
            var index = indexOf.call(buttons, service);
            if (index != -1) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        });
    }
    function getFeed(service, destination, result) {
        getLocation();
        var dynamicData = {};
        dynamicData["lat"] = lat;
        dynamicData["lng"] = lng;
        dynamicData["service"] = service;
        dynamicData["destination"] = destination;
        dynamicData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        return $.ajax({
            url: "../get_feed/",
            type: "get",
            data: dynamicData
        });
    }
    function fetchAllJourneys() {
        var feed = $("#nearest-buses").children();
        $.each(feed, function (key, value) {
            var result = $(this).find('.container-fluid');
            var service = result.attr('data-service');
            var destination = result.attr('data-destination');
            getFeed(service, destination, result).done(function (data) {
                result.empty();
                result.append(data);
            });
        });
    }
    function getServices() {
        return $("#nearest-buses").attr('data-feed');
    }
    function getButtons() {
        var buttons = getFilterButtons();
        return JSON.stringify(buttons);
    }
    function getFilterButtons() {
        var buttons = chosenDiv.children();
        if (buttons.length == 0) {
            buttons = availableDiv.children();
        }
        var buttons_data = [];
        $.each(buttons, function (key, value) {
            buttons_data.push($(this).text());
        });
        return buttons_data;
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
    setInterval(function () {
        fetchAllJourneys();
    }, 15000);
}));
//# sourceMappingURL=feed.js.map