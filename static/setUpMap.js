/**
 * Created by Sam Davies on 28/03/15.
 */

// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('tracker-map').setView([51.505, -0.09], 13);

// add an OpenStreetMap tile layer


// add a marker in the given location, attach some popup content to it and open the popup
L.marker([51.5, -0.09]).addTo(map)
    .bindPopup('A pretty CSS3 popup. <br> Easily customizable.')
    .openPopup();