import * as api from '../services/api';
import { logout } from '../actions/authActions';
import {
  SELECT_MEETING,
  MEETINGS_FETCH_SUCCESS,
  MEETING_CREATE_SUCCESS,
  MEETING_UPDATE_SUCCESS,
  MEETING_DELETE_SUCCESS,
  VOTE_CREATE_SUCCESS,
  VOTE_DELETE_SUCCESS,
  TIMESLOT_CREATE_SUCCESS,
  TIMESLOT_UPDATE_SUCCESS,
  TIMESLOT_DELETE_SUCCESS,
  REQUEST_ERROR,
} from "../constants/actionTypes";
  
  // Manage meeting successes
  export const selectMeeting = (id) => ({
    type: SELECT_MEETING,
    payload: id,
  });

  export const fetchMeetingsSuccess = (meetings) => ({
    type: MEETINGS_FETCH_SUCCESS,
    payload: meetings,
  });
  
  export const createMeetingSuccess = (meeting) => ({
    type: MEETING_CREATE_SUCCESS,
    payload: meeting,
  });

  export const updateMeetingSuccess = (meeting) => ({
    type: MEETING_UPDATE_SUCCESS,
    payload: meeting,
  });

  export const deleteMeetingSuccess = (meeting_id) => ({
    type: MEETING_DELETE_SUCCESS,
    payload: meeting_id,
  });
  
  // Manage vote success
  export const createVoteSuccess = (vote, timeslotId, meetingId) => ({
    type: VOTE_CREATE_SUCCESS,
    payload: { vote, timeslotId, meetingId },
  });

  export const deleteVoteSuccess = (voteId, timeslotId, meetingId) => ({
    type: VOTE_DELETE_SUCCESS,
    payload: { voteId, timeslotId, meetingId },
  });

  // Manage timeslot success
  export const createTimeSlotSuccess = (timeslot, meetingId) => ({
    type: TIMESLOT_CREATE_SUCCESS,
  payload: { timeslot, meetingId },
  });

  export const updateTimeSlotSuccess = (timeslot, meetingId) => ({
    type: TIMESLOT_UPDATE_SUCCESS,
  payload: { timeslot, meetingId },
  });

  export const deleteTimeSlotSuccess = (timeslotId, meetingId) => ({
    type: TIMESLOT_DELETE_SUCCESS,
  payload: { timeslotId, meetingId },
  });

  // Manage errors
  export const requestError = (error) => ({
    type: REQUEST_ERROR,
    payload: error,
  });  

  export const fetchMeeting = (id) => async (dispatch, getState) => {
    try {
      const response = await api.getMeeting(id);
      dispatch(selectMeeting(response.id));
  
      // Update the meeting in the array of meetings
      const { meetings } = getState().meeting;
      const meetingIndex = meetings.findIndex(meeting => meeting.id === id);
      const updatedMeetings = [...meetings];
      if (meetingIndex !== -1) {
        updatedMeetings[meetingIndex] = response;
      } else {
        updatedMeetings.push(response);
      }
      dispatch(fetchMeetingsSuccess(updatedMeetings));
    } catch (error) {
      if (error.message === 'Unauthorized') {
        dispatch(logout());
      } else {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      }
    }
  };

  export const fetchMeetings = () => async (dispatch) => {
    return await api.getMeetings()
      .then((response) => {
        dispatch(fetchMeetingsSuccess(response));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };
  
  export const createMeeting = (meeting) => async (dispatch) => {
    return await api.createMeeting(meeting)
      .then((response) => {
        dispatch(createMeetingSuccess(response));
        return response;
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };
  
  export const updateMeeting = (meeting) => async (dispatch) => {
    return await api.updateMeeting(meeting.id, meeting)
      .then((response) => {
        dispatch(updateMeetingSuccess(response));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };

  export const deleteMeeting = (id) => async (dispatch) => {
    return await api.deleteMeeting(id)
    .then(() => {
      dispatch(deleteMeetingSuccess(id));
    })
    .catch((error) => {
      if (error.message === 'Unauthorized') {
        dispatch(logout());
    } else {
        dispatch(requestError(error.toString()));
    }
    });
  }; 

  // Call votes api endpoint
  export const createVote = (vote) => async (dispatch) => {
    return await api.createVote({ timeslot_id: vote.timeslot_id })
      .then((response) => {
        dispatch(createVoteSuccess(response, vote.timeslot_id, vote.meeting_id));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };

  export const deleteVote = (vote) => async (dispatch) => {
    return await api.deleteVote(vote.vote_id)
      .then(() => {
        dispatch(deleteVoteSuccess(vote.vote_id, vote.timeslot_id, vote.meeting_id));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };

  // Call timeslots endpoint
  export const createTimeSlot = (timeslot) => async (dispatch) => {
    return await api.createTimeSlot(timeslot)
      .then((response) => {
        dispatch(createTimeSlotSuccess(response, timeslot.meeting_id));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };

  export const deleteTimeSlot = (timeslot) => async (dispatch) => {
    return await api.deleteTimeSlot(timeslot.timeslot_id)
      .then(() => {
        dispatch(deleteTimeSlotSuccess(timeslot.timeslot_id, timeslot.meeting_id));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };
  
  export const updateTimeSlot = (timeslot) => async (dispatch) => {
    return await api.updateTimeSlot(timeslot.id, timeslot)
      .then((response) => {
        dispatch(updateTimeSlotSuccess(response, timeslot.meeting_id));
      })
      .catch((error) => {
        if (error.message === 'Unauthorized') {
          dispatch(logout());
      } else {
          dispatch(requestError(error.toString()));
      }
      });
  };