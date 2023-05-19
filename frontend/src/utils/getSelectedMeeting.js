export const getSelectedMeeting = (state) => {
    return state.meeting.meetings.find(
      (meeting) => meeting.id === state.meeting.selectedMeetingId
    );
  };