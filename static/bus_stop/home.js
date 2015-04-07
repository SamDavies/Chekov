function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(saveLocation);
    }
    else {
        alert("Geolocation is not supported by this browser.");
    }
}
function saveLocation(position) {
    var lat = String(position.coords.latitude);
    var lng = String(position.coords.longitude);
    window.location.replace("/feed/?lat=" + lat + "&lng=" + lng);
}
getLocation();
//# sourceMappingURL=home.js.map