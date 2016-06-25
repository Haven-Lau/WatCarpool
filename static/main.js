$(document).ready(function() {
    console.log('ready');

    // Setup datatimepicker
	$('#datetimepicker').datetimepicker({
        defaultDate: moment(),
        format: 'h:mm A ddd YYYY-MM-DD'
    });

    // Not allowed to edit the content at the datatimepicker input field
    $('#date-time').on('keydown', function() {
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
    $('form').on('submit', function() {
		var from = $('input[id="from"]').val();
    	var to = $('input[id="to"]').val();
        var time = $('input[id="date-time"]').val();
        
    	console.log('Getting data: ' + from + ' to ' + to + ' at ' + time)

    	$.ajax({
    		type: 'POST',
    		url: '/',
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