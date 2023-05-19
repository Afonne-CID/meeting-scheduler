import { timeSlotShape, userShape, funcType } from '../utils/propTypes';
import { FaTrash } from 'react-icons/fa';
import Button from './Button';

const TimeSlot = ({ timeslot, user, handleVote, handleDeleteTimeslot }) => {
  const userVote = timeslot.votes.find(vote => vote.user_id === user.id);

  return (
    <div 
      key={timeslot.id} 
      className={`mb-4 bg-gray-100 rounded-lg 
      p-4 flex justify-between items-center`}
    >
      <div className='flex items-center'>
        <input 
          type="checkbox" 
          checked={!!userVote} 
          onChange={() => handleVote(timeslot)} 
        />
        <div 
          onClick={() => handleVote(timeslot)} 
          className={`
            ml-4 cursor-pointer px-4 py-2 rounded-lg flex 
            flex-row justify-between items-center 
            ${userVote ? 'bg-blue-500 text-white' 
            : 'bg-white'}`}>
          <div className=''>{timeslot.start_time} - {timeslot.end_time} 
            <span 
              className={
                `rounded-full ml-2 w-[100%] h-[100%] 
                ${userVote && 'bg-white text-blue-500'}`}
              >
              ({timeslot.votes.length} votes)
            </span>
          </div>
        </div>
      </div>
      <div>
        {timeslot.user_id === user.id && (
          !timeslot.votes || 
          timeslot.votes.length == 0 ||
          (timeslot.votes.length === 1 && userVote)
        ) && (
            <Button 
              onClick={() => handleDeleteTimeslot(timeslot.id)} 
              color="red-500" 
              hoverColor="red-700" 
              extraClasses="ml-3">
                <FaTrash />
            </Button>
        )}
      </div>
    </div>
  );
};

TimeSlot.propTypes = {
  timeslot: timeSlotShape.isRequired,
  user: userShape,
  handleVote: funcType,
  handleDeleteTimeslot: funcType,
};

TimeSlot.defaultProps = {
  user: {},
  handleVote: () => {},
  handleDeleteTimeslot: () => {},
};

export default TimeSlot;
