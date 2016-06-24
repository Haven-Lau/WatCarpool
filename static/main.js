$(document).ready(function() {
    console.log('ready');
	$('#datetimepicker').datetimepicker({
        defaultDate: moment()
    });
    $('form').on('submit', function() {
		var from = $('input[name="from"]').val();
    	var to = $('input[name="to"]').val();
    	console.log(from, to)

    	$.ajax({
    		type: 'POST',
    		url: '/',
    		data: {'fromdddd': from, 'to': to},
    		success: function(result) {
    			console.log('success');
    		},
    		error: function(error) {
    			console.log(error);
    		}
    	})
    })
});