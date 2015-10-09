$(function () {
	var Meeting = function (meeting) {
		this.title = ko.observable(meeting.title);
		this.text = ko.observable(meeting.text);
		this.editing = false;
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
				if (self.meetings().length > 0) {
					self.selectedMeeting(self.meetings()[0]);
				}
			});
		};

		this.selectMeeting = function (meeting) {
			self.selectedMeeting(meeting);
		};

		this.editText = function(meeting) {
			meeting.editing(true);
		}

		this.saveEditText = function(meeting) {
			meeting.editing(false);
		}

		this.saveEditText = function(meeting) {
			meeting.editing(false);
		}


		this.loadMeetings();
		
	};

	

	var m = new ViewModel();

	ko.applyBindings(m);

});