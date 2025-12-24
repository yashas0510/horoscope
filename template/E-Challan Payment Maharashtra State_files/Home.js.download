function intializeHomePage() {
	var parentElement;
	var visitorsWaiting = 0;
	var totalVisitors = 0;
	$.post('getNotificationForPa.htm', {
		locationId : locationId
	}, function(response) {
		var visitorCount = Object.keys(response).length;
		totalVisitors = visitorCount;
	});

	$.post('CountOfVisitorsToCp.htm', {
		locationId : locationId
	}, function(visitorsToCP) {
		totalVisitors = visitorsToCP + totalVisitors;
		$("#visitorCountForPa").text(totalVisitors);
	});

	$.post('CountOfVisitorsForwardedByPa.htm', {
		locationId : locationId
	}, function(visitorsForwardedByPa) {
		var visitorsForwardedByPa = visitorsForwardedByPa;
		$("#visitorsForwardedByPa").text(visitorsForwardedByPa);
	});

	$("#visitorCountForPa").click(function() {
		$.post('updateIsStatusChangedFlag.htm', {
			locationId : locationId
		}, function(response) {
			if (response == true) {
			}
		});
	});

	$("#visitorsForwardedByPa").click(function() {
		$.post('updateVisitorsForwardedByPaStatus.htm', {
			locationId : locationId
		}, function(response) {
			if (response == true) {
			}
		});
	});

	$('#myModal').modal({
		backdrop : 'static',
		keyboard : false,
		show : false
	});
	$.ajaxSetup({
		cache : false
	});
	$("#myTab a").click(function(e) {
		e.preventDefault();
		$(this).tab('show');
	});

	$(function() {
		$("input[type='checkbox']").change(
				function() {
					$(this).siblings('ul').find("input[type='checkbox']").prop(
							'checked', this.checked);
				});
	});

}