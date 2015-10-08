$(function () {
	var Meeting = function (meeting) {
		this.title = ko.observable(meeting.title);
		this.text = ko.observable(meeting.text);
	}
	var ViewModel = function () {
		var self = this;

		this.meetings = ko.observableArray();
		this.selectedMeeting = ko.observable();

		this.loadMeetings = function () {
			self.meetings = ko.observableArray();
			$.get('/meetinglist', function (data) {
				data.Meetings.forEach(function (meeting) {
					self.meetings.push(new Meeting(meeting));
				});
			});
		};

		this.selectMeeting = function (meeting) {
			self.selectedMeeting(meeting);
		};


		this.loadMeetings();
		if (this.meetings.length > 0) {
			this.currentMeeting(this.meetings()[0]);
		}
	};

	

	var m = new ViewModel();

	ko.applyBindings(m);

});