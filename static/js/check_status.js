var id_number = $('#id_endowmententity_set-' + rownum + '-id_number').val(),
url = '{% url check_print_status 0 %}'.replace('0', id_number);

console.log(url);

$.ajax({
	type: "GET",
	url: url,
	data: {
		'print_status': $("td.t11").val(),
	},
	dataType: "text",
	cache: false,
	success: function(data){
		if (data == 'ok'){
			console.log("ok")
		}
		else if (data == 'no'){
			console.log("no")
		}
	}
})