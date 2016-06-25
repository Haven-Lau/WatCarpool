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
    $('#reverse-loc').on('click', function()  {
        var from = $('input[id="from"]').val();
        var to = $('input[id="to"]').val();
        $('#from').val(to);
        $('#to').val(from);
    })

    // Ajax call to get post results
    $('#get-post').on('click', function() {
        console.log('click');
		var from = $('input[id="from"]').val();
    	var to = $('input[id="to"]').val();
        var time = $('input[id="date-time"]').val();
        
    	console.log('Getting data: ' + from + ' to ' + to + ' at ' + time)

    	$.ajax({
    		type: 'GET',
    		url: '/api/get-carpool-list',
    		data: {'from': from, 'to': to},
    		success: function(result) {
    			console.log(result);
    		},
    		error: function(error) {
    			console.log(error);
    		}
    	})
    })
});