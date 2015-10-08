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
				if (self.meetings.length() > 0) {
					self.selectedMeeting(self.meetings()[0]);
				}
			});
		};

		this.selectMeeting = function (meeting) {
			self.selectedMeeting(meeting);
		};


		this.loadMeetings();
		
	};

	

	var m = new ViewModel();

	ko.applyBindings(m);

});