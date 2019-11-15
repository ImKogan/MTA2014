$(document).ready(function(){

	function hourOptions(element) {
		element.append('<option value="" disabled selected>Hour</option>');
		element.append('<option value="0"><a href="#!">12 AM</a></option>');
		for (var i=1; i<12; i++) {
			var val = i.toString();
			element.append(
				'<option value="'+val+'"><a href="#!">'+i+'AM</a></option>'
			);
		}
		element.append('<option value="12"><a href="#!">12 PM</a></option>');
		for (var i=1; i<12; i++) {
			var j = i+12;
			var val = j.toString();
			element.append(
				'<option value="'+val+'"><a href="#!">'+i+'PM</a></option>'
			);
		}
	}

	hourOptions($('#select-hour'));

	function routeNameOptions (element, route_names) {
		element.append('<option value="" disabled selected>Route Name</option>');
		for (var i=0; i < route_names.length; i++) {
			var route = route_names[i];
			element.append('<option value='+route+'>'+route+'</option>');
		}
	}

	var route_names = window.route_names;
	routeNameOptions($('#select-route'), route_names)
		M.AutoInit();

	var dates = window.dates;
	dates.date__min = dates.date__min.toString();
	dates.date__max = dates.date__max.toString();
	var minDate = new Date(parseInt(dates.date__min.substring(0,4)),
					parseInt(dates.date__min.substring(4,6))-1,
					parseInt(dates.date__min.substring(6,8))
				)
	var maxDate = new Date(parseInt(dates.date__max.substring(0,4)),
					parseInt(dates.date__max.substring(4,6))-1,
					parseInt(dates.date__max.substring(6,8))
				)
	$(".datepicker").datepicker({
		container: $("#datepicker1-parent"),
		format: "yyyy-mm-dd",
		defaultDate: minDate,
		minDate: minDate,
		maxDate: maxDate
	});
	$(".timepicker").timepicker({timeFormat: 'h p',
		interval: 60,
		dynamic: false,
		scrollbar: true
	});
	$('select').formSelect();


		$("#submit-trip-query").click(function () {
			var $route = $("#select-route option:selected").val();
			console.log($route);
			var $direction = $("#select-direction").val();
			console.log($direction);
			var $date = $("#route-datepicker").val();
			console.log($date);
			var $hour = $("#select-hour").val();
			console.log($hour);

	        if (check_route_input($route, $direction, $date, $hour) == false){
	            return
	        }

			$.ajax({
				url: 'query_trips',
				data: {
					'route': $route,
					'direction': $direction,
					'date': $date,
					'hour': $hour,
				},
				dataType: 'text',
				success: function (response) {
					var uri = 'data:text/csv;charset=UTF-8,' + encodeURIComponent(response);
					// var uri = response.responseText
					// window.open(uri, 'trip.csv');
					// window.location = uri;
					var downloadLink = document.createElement("a");
					downloadLink.href = uri;
					downloadLink.download = "trip.csv";

					document.body.appendChild(downloadLink);
					downloadLink.click();
					document.body.removeChild(downloadLink);
					console.log(Date($date));
				},
				error: function(response) {
					console.log('error');
					console.log(response);
				}
			});
		});

});
