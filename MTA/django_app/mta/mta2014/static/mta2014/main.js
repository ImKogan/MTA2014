$(document).ready(function(){
	var accessKey = window.accessKey;
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
	hourOptions($('#select-hour-route'));
	hourOptions($('#select-hour-stop'));

	function routeNameOptions (element, route_names) {
		element.append('<option value="" disabled selected>Route Name</option>');
		for (var i=0; i < route_names.length; i++) {
			var route = route_names[i];
			element.append('<option value='+route+'>'+route+'</option>');
		}
	}
	
	var route_names = window.route_names;
	routeNameOptions($('#select_route'), route_names)

	M.AutoInit();
	//$('.tabs').tabs();
	$(".sidenav").sidenav({
		edge: 'right',
		ready: function() {
			$('.collapsible').collapsible({});
		}
	});
	$(".sidenav").sidenav('open');
	//$('.collapsible').collapsible({
	//	accordion: true
	//});
	$( ".tabs" ).tabs({
		active: 1
	});				  
				
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
		container: $("#datepicker-parent"),
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
	
	var mapsPlaceholder = []

	L.Map.addInitHook(function () {
		mapsPlaceholder.push($("#boros"));
	});
	var mymap = L.map("boros").setView([40.75, -73.95], 11);
	mymap.setMaxBounds([[40.5, -73.6], [41.0, -74.3]]);
	mymap.setMinZoom(10);
	mymap.setMaxZoom(15);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    	maxZoom: 18,
   		id: 'mapbox.streets',
    	accessToken: accessKey.mapbox
	}).addTo(mymap);

	var polygons_list = window.poly_list;
	for (var i=0; i < polygons_list.length; i++){
		var poly = $.parseJSON(polygons_list[i]);
		var coords = L.GeoJSON.coordsToLatLngs(poly.coordinates, 2);
		var polygon = L.polygon(coords).addTo(mymap);
	}

	var geojsonShapes = window.geoShapes;
	L.geoJson(geojsonShapes, {
		style: function(geojsonShapes) {
			var col = geojsonShapes.properties.route_name;
			return {className: 'mta-'+col.toLowerCase()}
		}
	}).addTo(mymap);
			
	var geojsonStops = window.geoStops;
	var geoJsonAllStops = new L.geoJson(geojsonStops, {
		pointToLayer: function (feature, latlng) {
			return new L.Circle(latlng, {
				color: 'black'
			});
		}
	}).addTo(mymap);
		
	var stops_dict = {};
	for (var i=0; i < geojsonStops.features.length; i++) {
		stops_dict[geojsonStops.features[i].properties.stop_name +
			" : " + geojsonStops.features[i].properties.stop_id] = null
	}
	$('input.autocomplete').autocomplete({
		data: stops_dict
	});
			
	function errorModal(response) {
		if (response.message !== undefined) {
			$("#error-message-modal .modal-content").append(
				'<p>'+response.message+'</p>');
			console.log(response.message);
			$('#error-message-modal').modal({
				onCloseEnd(){
				$('#error-message-modal	.modal-content p').remove();
				}
			});
			$('#error-message-modal').modal('open');
			return
		}
	}
	function time_null_check (time_string) {
		if (time_string != null) {
			return moment.tz(time_string*1000,
				"America/New_York").format("h:mm a")
		} else {
			return ""
		}
	}			

	function onEachFeature(feature, layer) {
		var stops_info = feature.properties.stops_info;
		if (feature.properties.route_id.slice(-1).toLowerCase() == 'x') {
			var lineX = '-x';
		} else {
			var lineX = '';
		}
		var popup_html = [
			'<div class="fixed">'+
			'<table>'+
			'<tr>'+
			'<th class="label-stop-info">Date: </th>'+
			'<th class="stop-info">'+feature.properties.date+'</th>'+
			'</tr>'+
			'<tr>'+
			'<th class="label-stop-info">Route ID: </th>'+
			'<th class="stop-info"><span class="mta-bullet'+lineX+' mta-'+
			feature.properties.route_id+'">'+
			'<span class="mta-text-'+feature.properties.route_id.toLowerCase()+'">'+
			feature.properties.route_id.slice(0,1)+'</span></span></th>'+
			'</tr>'+
			'<tr>'+
			'<th class="label-stop-info">Stop Name: </th>'+
			'<th class="stop-info">'+feature.properties.name+'</th>'+
			'</tr>'+
			'<tr>'+
			'<th class="label-stop-info">Stop ID: </th>'+
			'<th class="stop-info">'+feature.properties.stop_id+'</th>'+
			'</tr>'+
			'</table>'+
			'</div>'+
			'<div id="stop-data-collection-list">'
		];
		popup_html.push('<div class="collection">');
		for (var i =0; i < stops_info.length; i++) {
			popup_html.push(
				'<a href="#!" class ="collection-item">'+
				'<table class="striped" id="stop-data">'+
				'<tbody>'+
				'<tr>'+
				'<td class="label-stop-info"><b>Arrival: </b></td>'+ 
				'<td class="stop-info">'+time_null_check(stops_info[i].arrival)+'</td>'+
				'</tr>'+
				'<tr>'+
				'<td class="label-stop-info"><b>Departure: </b></td>'+
				'<td class="stop-info">'+time_null_check(stops_info[i].departure)+'</td>'+
				'</tr>'+
				'</tbody>'+
				'</table>'
			);
		}
		popup_html.push('</div></div>');
		layer.bindPopup(
			popup_html.join(''),
			{className: 'stop-popup',
			maxHeight: 400,
		  	closeButton: false,
		   	offset: L.point(0, 7)});
			//layer.on('mouseover', function() { layer.openPopup(); });
            //layer.on('mouseout', function() { layer.closePopup(); });
	}
			
	function stopTimes(feature) {
		var modalTable = $("#modal-stop-info #header-table");
		modalTable.append(
			'<tr>'+
			'<th class="label-stop-info">Date: </th>'+
			'<th class="stop-info">'+feature.properties.date+'</th>'+
			'</tr>'+
			'<tr>'+
			'<th class="label-stop-info">Stop Name: </th>'+
			'<th class="stop-info">'+feature.properties.stop_name+'</th>'+
			'</tr>'+
			'<tr>'+
			'<th class="label-stop-info">Stop ID: </th>'+
			'<th class="stop-info">'+feature.properties.stop_id+'</th>'+
			'</tr>'
		);
		modalTable.append(
			'<a href="#!" class ="collection-item">'+
			'<table class="striped" id="stop-data">'+
			'<tbody>'
		);

		var trips = feature.properties.trips;
			$.each(
				trips,
				function(i, trip) {
					if (trip.stop_id.slice(-1).toLowerCase() == 'n') {
						var modalTable = $("#modal-stop-info #north-direction tbody");
					} else {
						var modalTable = $("#modal-stop-info #south-direction tbody");
					}
					if (trip.route_id.slice(-1).toLowerCase() == 'x') {
						var lineX = '-x';
					} else {
						var lineX = '';
					}
					console.log(lineX);
					modalTable.append(
						'<tr>'+
						'<td class="stop-info"><span class="mta-bullet'+lineX+' mta-'+
						trip.route_id+'">'+
						'<span class="mta-text-'+trip.route_id.toLowerCase()+'">'+
						trip.route_id.slice(0,1)+'</span></span></td>'+
						'<td class="stop-info">'+trip.stop_id+'</td>'+
						'<td class="stop-info">'+time_null_check(trip.arrival)+'</td>'+
						'<td class="stop-info">'+time_null_check(trip.departure)+'</td>'+
						'</tr>'
					)
				}
			);
	}

	$("#submit_route_search").click(function () {
		console.log(mymap);
		var $route = $("#select_route option:selected").val();
		console.log($route);
		var $direction = $("#select_direction").val();
		console.log($direction);
		var $date = $("#route-datepicker").val();
		console.log($date);
		var $hour = $("#select-hour-route").val();				
		console.log($hour);

		$.ajax({
			url: 'route_stops',
			data: {
				'route': $route,
				'direction': $direction,
				'date': $date,
				'hour': $hour,
			},
			dataType: 'json',
			success: function (response) {
				if (typeof(geojsonLayerStops) === 'object') {
					mymap.removeLayer(geojsonLayerStops);
				}
				if (typeof(geojsonLayerShapes) === 'object') {
					mymap.removeLayer(geojsonLayerShapes);
				}						
				errorModal(response);
				var geojsonFeatureShapes = response.shapes_json;
				geojsonLayerShapes = L.geoJson(
					geojsonFeatureShapes, {
						style: function(geojsonFeatureShapes) {
							var col = geojsonFeatureShapes.properties.route_name;
							return {
								className: 'mta-'+col.toLowerCase(),
								weight: 6
							}
						}
				});
				geojsonLayerShapes.addTo(mymap);

				var geojsonFeatureStops = response.stops_json;
				geojsonLayerStops = L.geoJson(geojsonFeatureStops, {
					onEachFeature: onEachFeature,
					pointToLayer: function (feature, latlng) {
						return L.circleMarker(latlng, {
							radius: 5
						});
					}
				});
				geojsonLayerStops.addTo(mymap);
				console.log(Date($date));
			}
		});
	});
			
	$("#submit_stop_search").click(function () {
		var $stop = $("#stop-name-input").val();
		var $date = $("#stop-datepicker").val();
		console.log($date);
		var $hour = $("#select-hour-stop").val();				

		$.ajax({
			url: 'stop_times',
			data: {
				'stop': $stop,
				'date': $date,
				'hour': $hour,
			},
			dataType: 'json',
			success: function (response) {
				$("#modal-stop-info #header-table").empty();
				$("#north-direction tbody").empty();
				$("#south-direction tbody").empty();
				if (typeof(geojsonLayerStops) === 'object') {
					mymap.removeLayer(geojsonLayerStops);
				}
				if (typeof(geojsonLayerShapes) === 'object') {
					mymap.removeLayer(geojsonLayerShapes);
				}
				errorModal(response);
				var modalTrigger = '<a class="modal-trigger" id="modal-stop-info-trigger" href="#modal-stop-info">click for stop schedule</a>'
				var geojsonFeatureStops = response.stops_json;
				geojsonLayerStops = L.geoJson(geojsonFeatureStops, {
					pointToLayer: function (feature, latlng) {
						stopTimes(feature);
						return L.circleMarker(latlng, {
							radius: 8
						});
					}
				}).bindPopup(modalTrigger)
				geojsonLayerStops.addTo(mymap).openPopup();
				$('#modal-stop-info').modal('open');
				console.log(Date($date));
			}
		});
	});
});
