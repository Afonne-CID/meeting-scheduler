import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import Button from './Button';
import CopyUrl from './CopyUrl';
import { fetchMeeting } from '../actions/meetingActions';
import { meetingShape, funcType } from '../utils/propTypes';
import { deleteMeeting } from '../actions/meetingActions';

function MeetingCard({ meeting }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector(state => state.auth.user) || {};

  const handleViewMeeting = () => {
    dispatch(fetchMeeting(meeting.id));
    navigate(`/meetings/${meeting.id}`);
  };

  const handleDeleteMeeting = () => {
    dispatch(deleteMeeting(meeting.id));
  }

  const meetingUrl = `${window.location.origin}/meetings/${meeting.id}`;

  return (
    <div 
      className={`
        meeting-card rounded overflow-hidden shadow-lg p-6 
        bg-white hover:shadow-xl transition-shadow 
        duration-300 ease-in-out`}
    >
      <h2 className="font-bold text-xl mb-2">{meeting.title}</h2>
      <p className="text-gray-700 text-base">{meeting.description}</p>
      <CopyUrl meetingUrl={meetingUrl} />
      <div className='flex flex-row justify-between'>
        <Button 
          onClick={handleViewMeeting} 
          color="blue-500" 
          hoverColor="blue-700" 
          extraClasses="font-bold py-2 px-4 rounded mt-4 ml-2">
            View Meeting
        </Button>
        {meeting.user_id == user.id && (
          <Button 
            onClick={handleDeleteMeeting} 
            color="red-500" 
            hoverColor="red-700" 
            extraClasses="font-bold py-2 px-4 rounded mt-4">
              Delete Meeting
          </Button>
        )}
      </div>
    </div>
  );  
}

MeetingCard.propTypes = {
  meeting: meetingShape.isRequired,
  handleClick: funcType
};

export default MeetingCard;
