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

function check_route_input($route, $direction, $date, $hour) {
		message = {}
		string_array = []
		if ($route == ''){
				string_array.push('Please choose a Route')
		}
		if ($direction == null){
				string_array.push('Please choose a Direction')
		}
		if ($date == ''){
				string_array.push('Please choose a Date')
		}
		if ($hour == null){
				string_array.push('Please choose a Hour')
		}
		if (string_array.length > 0) {
				message['message'] = string_array.join("<br>")
				errorModal(message)
		}

		if (Object.keys(message).length === 0){
				return true
		}
		return false
}

