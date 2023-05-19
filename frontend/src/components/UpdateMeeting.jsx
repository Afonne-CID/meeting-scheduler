import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import Timeslot from './TimeSlot';
import Button from './Button';
import Header from './Header';
import StatusMessage from './StatusMessage';
import { meetingShape } from '../utils/propTypes';
import { getSelectedMeeting } from '../utils/getSelectedMeeting';
import { clearError, clearSuccess } from '../actions';
import { 
  updateMeeting, 
  fetchMeeting, 
} from '../actions/meetingActions';


const UpdateMeeting = () => {
  const [meeting, setMeeting] = useState({ title: '', description: '', timeslots: [] });
  const { meeting_id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const meetingData = useSelector(state => getSelectedMeeting(state));
  const user = useSelector(state => state.auth.user);

  // Reset error and success messages
  useEffect(() => {
    dispatch(clearError());
    dispatch(clearSuccess())
  }, [dispatch]); 

  useEffect(() => {
    dispatch(fetchMeeting(meeting_id))
  }, [dispatch, meeting_id]);

  // Destructure the properties from meetingData
  const { id, title, description, timeslots } = meetingData || {};

  // Use these destructured properties as dependencies
  useEffect(() => {
    setMeeting({
      id: id || null, 
      title: title || '', 
      description: description || '', 
      timeslots: timeslots || []
    });
  }, [id, title, description, timeslots]);  

  const handleChange = (e) => {
    setMeeting({
      ...meeting,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(updateMeeting(meeting))
    navigate(`/meetings/${meeting_id}`);
  };

  return (
    <div 
      className={
        `w-full meeting-page container 
        mx-auto px-4 sm:px-6 lg:px-8 bg-white 
        rounded-lg shadow p-6`}
    >
      <Header />
      <StatusMessage />
      <form onSubmit={handleSubmit} className="w-full max-w-lg mx-auto mt-5">
        <div className="mb-4">
          <label 
            className="block text-gray-700 text-sm font-bold mb-2" 
            htmlFor="title"
          >
            Title
          </label>
          <input
            type="text"
            name="title"
            id="title"
            value={meeting.title}
            onChange={handleChange}
            className={`
              shadow appearance-none border rounded w-full 
              py-2 px-3 text-gray-700 leading-tight 
              focus:outline-none focus:shadow-outline`}
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="description">
            Description
          </label>
          <textarea
            name="description"
            id="description"
            value={meeting.description}
            onChange={handleChange}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-20"
          />
        </div>
        <h3>Suggested Times</h3>
        <div className="opacity-50 pointer-events-none">
          {meeting.timeslots && meeting.timeslots.map(timeslot => (
            <Timeslot 
              key={timeslot.id} 
              timeslot={timeslot} 
              user={user}
            />
          ))}
        </div>
        <div className="flex mt-4 items-center justify-between">
          <Button type="submit">Submit Update</Button>
        </div>
      </form>
    </div>
  );
};

UpdateMeeting.propTypes = {
  meeting: meetingShape
};

export default UpdateMeeting;
