$(document).ready(function() {
    console.log('ready');

    // Setup datatimepicker
	$('#datetimepicker1').datetimepicker({
        defaultDate: moment(),
    });

    $('#date-of-carpool').datetimepicker({
        defaultDate: moment(),
    });

    // Not allowed to edit the content at the datatimepicker input field
    $('#date-time').on('keydown', function() {
        return false;
    })

    $('#date-of-carpool').on('keydown', function() {
        return false;
    })

    // Reverse location
    //$('#reverse-loc').on('click', function()  {
    //    var from = $('input[id="origin-search"]').val();
    //    var to = $('input[id="destination-search"]').val();
    //    $('#origin-search').val(to);
    //    $('#destination-search').val(from);
    //})

    // Ajax call to post carpool
    $('#post-carpool').on('click', function() {
        var originCity = $('input[id="origin-city"]').val();
        var destinationCity = $('input[id="destination-city"]').val();
        var dateOfCarpool = parseDate($('input[id="date-of-carpool"]').val());
        var now = parseDate(new Date());
        var price = $('input[id="price"]').val();
        var availableSpot = $('input[id="available-spots"]').val();
        var pickUpLocation = $('input[id="pick-up-location"]').val();
        var dropOffLocation = $('input[id="drop-off-location"]').val();
        var phoneNumber = $('input[id="phone-number"]').val();

        console.log(originCity, destinationCity, dateOfCarpool, price, availableSpot, pickUpLocation, dropOffLocation, phoneNumber, now);

        $.ajax({
            type: 'POST',
            url: '/api/post-carpool',
            data: {
                'phone-number': phoneNumber,
                'num-spots': availableSpot,
                'origin': originCity,
                'destination': destinationCity,
                'publish-date-time': now,
                'carpool-date-time': dateOfCarpool,
                'pick-up': pickUpLocation,
                'drop-off': dropOffLocation,
                'price': price
            },
            success: function(result) {
                console.log('success');
            },
            error: function(error) {
                console.log(error);
            }
        })
    });
});

var myApp = angular.module('myApp', ['ngScrollable']);
myApp.controller('controller', function($scope, $http) {
    $scope.getCarpool = function(reverse) {
        if (reverse) {
            var from = $('input[id="origin-search"]').val();
            var to = $('input[id="destination-search"]').val();
            $('#origin-search').val(to);
            $('#destination-search').val(from);
        }
        var originSearch = $('input[id="origin-search"]').val();
        var destinationSearch = $('input[id="destination-search"]').val();
        $http.get('/api/get-carpool-list', {
                params: {
                    'from': originSearch,
                    'to': destinationSearch
                },
            })
            .then(function(response) {
                $scope.lists = response.data.result;
            });
    };    
});

function parseDate(s) {
    var date = moment(s);
    return date.format('YYYY-MM-DD HH:mm:ss')
}
