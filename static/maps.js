var map;

function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;

    // Initialize the map
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 43.473,
            lng: -80.541
        },
        zoom: 15
    });
    directionsDisplay.setMap(map);
    var onChangeHandler = function() {
          calculateAndDisplayRoute(directionsService, directionsDisplay);
    };
    document.getElementById('get-carpool').addEventListener('click', onChangeHandler);
    document.getElementById('reverse-loc').addEventListener('click', onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: document.getElementById('origin-search').value.toLowerCase().includes('waterloo') ? 
            '150 University Ave West, Waterloo' : document.getElementById('origin-search').value,
        destination: document.getElementById('destination-search').value + ' canada',
        travelMode: google.maps.TravelMode.DRIVING
    }, function(response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}