$(function () {
	var ViewModel = function () {
		this.meetings = ko.observableArray();
		this.data = ko.observable();
		this.loadMeetings();
	};

	ViewModel.prototype.loadMeetings = function () {
		$.ajax({
			url: '/meetinglist',
			method: 'GET',
			done: function (data) {
				this.json(data);
			}
		});
	};

	var m = new ViewModel();

	ko.applyBindings(m);

});