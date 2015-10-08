$(function () {
	var Meeting = function (meeting) {
		this.title = ko.observable(meeting.title);
		this.text = ko.observable(meeting.text);
	}
	var ViewModel = function () {
		this.meetings = ko.observableArray();
		this.json = ko.observable();
		this.loadMeetings();
	};

	ViewModel.prototype.loadMeetings = function () {
		var self = this;
		self.meetings = ko.observableArray();
		$.get('/meetinglist', function (data) {
			data.Meetings.forEach(function (meeting) {
				self.meetings.push(new Meeting(meeting));
			});
		});
	};

	var m = new ViewModel();

	ko.applyBindings(m);

});