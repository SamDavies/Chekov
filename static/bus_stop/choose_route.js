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
    var lat = '0';
    var lng = '0';
    availableDiv.on("click", "button", function () {
        addButton($(this).text(), chosenDiv, "btn btn-primary");
        $(this).remove();
        getFeed();
    });
    chosenDiv.on("click", "button", function () {
        addButton($(this).text(), availableDiv, "btn btn-default");
        $(this).remove();
        getFeed();
    });
    function addButton(button, div, cssClass) {
        var buttonHTML = '<button type="button" class="' + cssClass + '">' + button + '</button> ';
        div.prepend(buttonHTML);
    }
    function getFeed() {
        getLocation();
        var dynamicData = {};
        dynamicData["lat"] = lat;
        dynamicData["lng"] = lng;
        dynamicData["services"] = getServices();
        dynamicData["buttons"] = getButtons();
        dynamicData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        return $.ajax({
            url: "get_feed/",
            type: "post",
            data: dynamicData
        });
    }
    getFeed().done(function (data) {
        // Updates the UI based the ajax result
        var feed = $("#nearest-buses");
        feed.empty();
        feed.append(data);
    });
    function getServices() {
        return $("#nearest-buses").attr('data-feed');
    }
    function getButtons() {
        var buttons = chosenDiv.children();
        if (buttons.length == 0) {
            buttons = availableDiv.children();
        }
        var buttons_data = [];
        $.each(buttons, function (key, value) {
            buttons_data.push($(this).text());
        });
        alert(buttons_data);
        return JSON.stringify(buttons_data);
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
}));
//# sourceMappingURL=choose_route.js.map