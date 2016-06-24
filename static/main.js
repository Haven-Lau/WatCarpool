$(document).ready(function() {
    console.log('ready');
	$('#datetimepicker').datetimepicker({
        defaultDate: moment()
    });
    $('form').on('submit', function() {
		valueOne = $('input[name="from"]').val();
    	valueTwo = $('input[name="to"]').val();
    	console.log(valueOne, valueTwo)

    	$.ajax({
    		type: 'POST',
    		url: '/',
    		data: {'first': valueOne, 'second': valueTwo},
    		success: function(result) {
    			console.log(result);
    		},
    		error: function(error) {
    			console.log(error);
    		}
    	})
    })
});