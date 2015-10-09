$(function () {
	
	// wrapper to hasFocus that also selects text and applies focus async
	ko.bindingHandlers.selectAndFocus = {
		init: function (element, valueAccessor, allBindingsAccessor, bindingContext) {
			ko.bindingHandlers.hasFocus.init(element, valueAccessor, allBindingsAccessor, bindingContext);
			ko.utils.registerEventHandler(element, 'focus', function () {
				element.focus();
			});
		},
		update: function (element, valueAccessor) {
			ko.utils.unwrapObservable(valueAccessor()); // for dependency
			// ensure that element is visible before trying to focus
			setTimeout(function () {
				ko.bindingHandlers.hasFocus.update(element, valueAccessor);
			}, 0);
		}
	};

	var Meeting = function (meeting) {
		this.id = meeting.id;
		this.title = ko.observable(meeting.title);
		this.text = ko.observable(meeting.text);
		this.editing = ko.observable(false);
		this.save = function () {
			$.post('/meeting/' + this.id, {
				text: this.text()
			});
		};
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

		this.editMeetingText = function(meeting) {
			meeting.editing(true);
		}

		this.saveEditMeetingText = function(meeting) {
			meeting.editing(false);
		}

		this.saveEditMeetingText = function(meeting) {
			meeting.save();
			meeting.editing(false);
		}


		this.loadMeetings();
		
	};

	

	var m = new ViewModel();

	ko.applyBindings(m);



});