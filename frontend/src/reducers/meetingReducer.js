import {
  SELECT_MEETING,
  MEETING_CREATE_SUCCESS,
  MEETING_UPDATE_SUCCESS,
  MEETING_DELETE_SUCCESS,
  VOTE_CREATE_SUCCESS,
  VOTE_DELETE_SUCCESS,
  TIMESLOT_CREATE_SUCCESS,
  TIMESLOT_UPDATE_SUCCESS,
  TIMESLOT_DELETE_SUCCESS,
  MEETINGS_FETCH_SUCCESS,
  REQUEST_ERROR,
  CLEAR_ERROR,
  CLEAR_SUCCESS,
} from "../constants/actionTypes";

const initialState = {
  meetings: [],
  selectedMeetingId: null,
  error: null,
  success: null,
};

export default function meetingReducer(state = initialState, action) {
  switch (action.type) {
    case SELECT_MEETING:
      return {
        ...state,
        selectedMeetingId: action.payload,
      };
    case MEETINGS_FETCH_SUCCESS:
      return {
        ...state,
        meetings: action.payload,
      };
    case MEETING_CREATE_SUCCESS:
      return {
        ...state,
        meetings: [...state.meetings, action.payload],
        success: 'Meeting created successfully!',
        error: null,
      };
    case MEETING_UPDATE_SUCCESS:
      return {
        ...state,
        meetings: state.meetings.map(meeting =>
          meeting.id === action.payload.id ? action.payload : meeting
        ),
        success: 'Meeting updated successfully!',
        error: null,
      };
    case MEETING_DELETE_SUCCESS:
      return {
        ...state,
        meetings: state.meetings.filter(meeting => meeting.id !== action.payload),
        success: 'Meeting deleted successfully!',
        error: null,
      };
    case VOTE_CREATE_SUCCESS: {
      const { vote, timeslotId, meetingId } = action.payload;
      return {
        ...state,
        meetings: state.meetings.map(meeting =>
          meeting.id === meetingId
            ? { 
                ...meeting, 
                timeslots: meeting.timeslots.map(timeslot =>
                  timeslot.id === timeslotId
                    ? { ...timeslot, votes: [...timeslot.votes, vote] }
                    : timeslot
                )
              }
            : meeting
        ),
        success: 'Vote created successfully!',
        error: null,
      };
    } 
    case VOTE_DELETE_SUCCESS: {
      const { voteId, timeslotId, meetingId } = action.payload;
      return {
        ...state,
        meetings: state.meetings.map(meeting =>
          meeting.id === meetingId
            ? { 
                ...meeting, 
                timeslots: meeting.timeslots.map(timeslot =>
                  timeslot.id === timeslotId
                    ? { ...timeslot, votes: timeslot.votes.filter(vote => vote.id !== voteId) }
                    : timeslot
                )
              }
            : meeting
        ),
        success: 'Vote deleted successfully!',
        error: null,
      };
    }    
    case TIMESLOT_CREATE_SUCCESS: {
      const { timeslot, meetingId } = action.payload;
      return {
        ...state,
        meetings: state.meetings.map(meeting =>
          meeting.id === meetingId
            ? { ...meeting, timeslots: [...meeting.timeslots, timeslot] }
            : meeting
        ),
        success: 'TimeSlot created successfully!',
        error: null,
      };
    }
    case TIMESLOT_UPDATE_SUCCESS: {
      const { timeslot, meetingId } = action.payload;
      return {
        ...state,
        meetings: state.meetings.map(meeting => 
          meeting.id === meetingId
            ? { ...meeting, 
                timeslots: meeting.timeslots.map(slot => 
                  slot.id === timeslot.id ? timeslot : slot) }
            : meeting
        ),
        success: 'TimeSlot updated successfully!',
        error: null,
      };
    }
    case TIMESLOT_DELETE_SUCCESS: {
      const { timeslotId, meetingId } = action.payload;
      return {
        ...state,
        meetings: state.meetings.map(meeting => 
          meeting.id === meetingId
            ? { ...meeting, timeslots: meeting.timeslots.filter(slot => slot.id !== timeslotId) }
            : meeting
        ),
        success: 'TimeSlot deleted successfully!',
        error: null,
      };
    }
    case REQUEST_ERROR:
      return {
        ...state,
        error: action.payload,
        success: null,
      };
    case CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    case CLEAR_SUCCESS:
      return {
        ...state,
        success: null,
      };
    default:
      return state;
  }
}
