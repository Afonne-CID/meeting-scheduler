import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import { FaPlus } from 'react-icons/fa';
import Timeslot from './TimeSlot';
import CopyUrl from './CopyUrl';
import Button from './Button';
import Header from './Header';
import Loading from './Loading';
import NotFound from './NotFound';
import StatusMessage from './StatusMessage';
import { meetingShape } from '../utils/propTypes';
import { getSelectedMeeting } from '../utils/getSelectedMeeting';
import { clearError, clearSuccess } from '../actions';
import {
  fetchMeeting,
  createTimeSlot,
  createVote,
  deleteVote,
  deleteTimeSlot,
} from '../actions/meetingActions';

const MeetingPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { meeting_id } = useParams();
  const meeting = useSelector(state => getSelectedMeeting(state));
  const user = useSelector(state => state.auth.user) || {};

  const [newStartTime, setNewStartTime] = useState('');
  const [newEndTime, setNewEndTime] = useState('');
  const [loading, setLoading] = useState(true);

    // Reset error and success messages
  useEffect(() => {
    dispatch(clearError());
    dispatch(clearSuccess())
  }, [dispatch]); 

  useEffect(() => {
    dispatch(fetchMeeting(meeting_id));
    setLoading(false);
  }, [dispatch, meeting_id]);

  if (loading) {
    return <Loading />;
  }

  if (!meeting) {
    return <NotFound />;
  }

  const handleCreateTimeslot = (timeslotData) => {
    if (!timeslotData.startTime || !timeslotData.endTime) {
      alert('Start and end times cannot be empty');
      return;
    } else if(new Date(timeslotData.startTime) >= new Date(timeslotData.endTime)) {
      alert('Start time must be less than end time');
      return
    }
    dispatch(createTimeSlot(timeslotData));
  };

  const handleVote = (timeslot) => {
    // Check if user has already voted on this timeslot
    const userVote = timeslot.votes.find(vote => vote.user_id === user.id);
    if (userVote) {
      dispatch(deleteVote({
        vote_id: userVote.id,
        timeslot_id: userVote.timeslot_id,
        meeting_id: meeting.id
      }));
    } else {
      dispatch(createVote({ meeting_id: meeting.id, timeslot_id: timeslot.id }));
    }
  };

  const handleDeleteTimeslot = (timeslotId) => {
    dispatch(deleteTimeSlot({ timeslot_id: timeslotId, meeting_id: meeting.id }));
  };

  const handleUpdateMeeting = () => {
    dispatch(fetchMeeting(meeting.id));
    navigate(`/update-meeting/${meeting.id}`);
  };

  const meetingUrl = `${window.location.origin}/meetings/${meeting_id}`;
  const minDateTime = new Date().toISOString().slice(0, 16);

  return (
    <div className={`
      meeting-page container mx-auto px-4 sm:px-6 
      lg:px-8 bg-white rounded-lg shadow p-6 mt-2`}
    >
      <Header />
      <StatusMessage />
      <h2 className="font-bold text-2xl mb-4">{meeting.title}</h2>
      <div className="flex flex-row items-center mb-4">
        <span className="font-bold mr-2">Url: </span>
        <CopyUrl meetingUrl={meetingUrl} />
      </div>
      <p className="text-gray-700 text-base mb-4">{meeting.description}</p>

      <h3>Suggested Times</h3>
      {meeting.timeslots && meeting.timeslots.map(timeslot => (
        <Timeslot 
          key={timeslot.id} 
          timeslot={timeslot} 
          user={user} 
          handleVote={handleVote} 
          handleDeleteTimeslot={handleDeleteTimeslot}
        />
      ))}
      {!meeting.final_time && (
        <div className="flex flex-col sm:flex-row justify-center">
          <input 
            type="datetime-local" 
            placeholder="New start time" 
            value={newStartTime} 
            min={minDateTime}
            onChange={(e) => setNewStartTime(e.target.value)} 
            className={`
              shadow appearance-none border rounded w-full 
              py-2 px-3 text-gray-700 leading-tight 
              focus:outline-none focus:shadow-outline mb-2`} 
          />
          <input 
            type="datetime-local" 
            placeholder="New end time" 
            value={newEndTime} 
            min={minDateTime}
            onChange={(e) => setNewEndTime(e.target.value)} 
            className={`
              p-4 shadow appearance-none border rounded 
              w-full py-2 px-3 text-gray-700 leading-tight 
              focus:outline-none focus:shadow-outline mb-2`} 
          />
          <button 
            onClick={() => handleCreateTimeslot({
              meeting_id: meeting.id, 
              startTime: newStartTime, 
              endTime: newEndTime }
            )} 
            className={`
              ml-2 bg-blue-500 hover:bg-blue-700 text-white 
              font-bold py-2 px-4 rounded flex justify-center items-center`}
          >
            <FaPlus />
          </button>
        </div>
      )}
      {!meeting.final_time && user.id === meeting.user_id && (
        <div className='mt-4'>
          <Button onClick={handleUpdateMeeting}>Update Meeting</Button>
        </div>
      )}
    </div>
  );
}

MeetingPage.propTypes = {
  meeting: meetingShape
};

export default MeetingPage;

