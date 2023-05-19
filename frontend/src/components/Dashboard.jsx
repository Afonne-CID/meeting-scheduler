import { useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from 'react-redux';
import { fetchMeetings } from '../actions/meetingActions';
import { clearError, clearSuccess } from '../actions';
import MeetingCard from './MeetingCard';
import Button from './Button';
import Header from './Header';
import StatusMessage from './StatusMessage';

function Dashboard() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const meetings = useSelector(state => state.meeting.meetings);

  // Reset error and success messages
  useEffect(() => {
    dispatch(clearError());
    dispatch(clearSuccess())
}, [dispatch]); 

  const handleCreateMeeting = () => {
    navigate("/create-meeting");
  };

  useEffect(() => {
    dispatch(fetchMeetings());
  }, [dispatch]);

  return (
    <div className="dashboard container mx-auto px-4 sm:px-6 lg:px-8 my-4">
      <Header />
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        Your Meetings
      </h1>
      <Button onClick={handleCreateMeeting}>Create Meeting</Button>
      <div className='mt-4 flex text-center justify-center'>
        <StatusMessage />
      </div>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {meetings.length > 0 ? (
          meetings.map((meeting, index) => 
            <MeetingCard 
              key={index} 
              meeting={meeting} 
              className={
                `shadow-lg rounded-2xl p-4 bg-white dark:bg-gray-800 w-full`}
            />
          )
        ) : (
          <p className="text-gray-700 text-base">
            No meetings found. Create a new one?
          </p>
        )}
      </div>
    </div>
  );   
}

export default Dashboard;
