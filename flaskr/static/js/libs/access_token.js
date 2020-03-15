$(document).ready(function() {
	var server = "http://127.0.0.1:5000";
	var appdir = "/process"

	if(window.location.hash){
		var hash = window.location.hash.substr(1);

		$.ajax({
			type: "POST",
			url: server+appdir,
			data: JSON.stringfy(hash),
			dataType: 'json'
		}).done(function(data) {
			console.log(data);
		});
	};
});