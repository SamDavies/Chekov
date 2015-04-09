/* Tracker Map */

class TrackerMap {
    
    map: any;
    marker: any;
    
    constructor(mapId: string) {
        var map = L.map(mapId);
        
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        var marker = L.marker([0, 0]).addTo(map);
        
        this.map = map;
        this.marker = marker;
    }
    
    setLocation(x: number, y: number) {
        this.map.setView([x, y]);
        
        this.map.removeLayer(this.marker);
        this.marker = L.marker([x, y]).addTo(map);
        this.marker.bindPopup("<b>You are here!</b>");
    }
    
}