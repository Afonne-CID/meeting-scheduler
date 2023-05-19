import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { MdDelete, MdAdd } from "react-icons/md";
import Header from './Header';
import { createMeeting } from '../actions/meetingActions';
import { clearError, clearSuccess } from '../actions';

const CreateMeeting = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [timeSlots, setTimeSlots] = useState([{ startTime: '', endTime: '' }]);
  const meetingError = useSelector(state => state.meeting.error);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  // Reset error and success messages
  useEffect(() => {
    dispatch(clearError());
    dispatch(clearSuccess())
  }, [dispatch]); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    for (let i = 0; i < timeSlots.length; i++) {
      if (!timeSlots[i].startTime || !timeSlots[i].endTime) {
        alert('Start and end time must not be empty');
        return
      } else if (timeSlots[i].startTime >= timeSlots[i].endTime) {
        alert('End time must be greater than start time');
        return;
      }
    }
    const response = await dispatch(createMeeting({ title, description, timeSlots }));
    navigate(`/meetings/${response.id}`);
  };

  const handleAddTimeSlot = () => {
    setTimeSlots([...timeSlots, { startTime: '', endTime: '' }]);
  };

  const handleRemoveTimeSlot = (index) => {
    setTimeSlots(timeSlots.filter((_, i) => i !== index));
  };

  const handleTimeSlotChange = (index, field, value) => {
    const newTimeSlots = [...timeSlots];
    newTimeSlots[index][field] = value;
    setTimeSlots(newTimeSlots);
  };

  // Set minimum allowed datetime to current datetime
  const minDateTime = new Date().toISOString().slice(0, 16);

  return (
    <div className="max-w-lg sm:mx-auto mt-5 mx-4">
      <Header />
      <h1 className="text-2xl font-bold mb-5 text-center">
        Create a New Meeting
      </h1>
      {meetingError && (
        <div className="text-red-500 bg-gray-100">
          {meetingError}
        </div>
      )}
      <form onSubmit={handleSubmit} className="w-full">
        <div className="mb-4">
          <label 
            className="block text-gray-700 text-sm font-bold mb-2" 
            htmlFor="title"
          >
            Title
          </label>
          <input 
            type="text" 
            id="title"
            placeholder='Meeting title'
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            required 
            className={`
              shadow appearance-none border rounded w-full 
              py-2 px-3 text-gray-700 leading-tight 
              focus:outline-none focus:shadow-outline`}
          />
        </div>
        <div className="mb-4">
          <label 
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="description"
          >
            Description
          </label>
          <textarea 
            id="description"
            placeholder='Meeting description'
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
            required 
            className={`
              shadow appearance-none border rounded w-full py-2 px-3 
              text-gray-700 leading-tight focus:outline-none 
              focus:shadow-outline h-20`}
          />
        </div>
        {timeSlots && timeSlots.map((timeSlot, index) => (
          <div key={index} className="mb-4">
            <div 
              className={`
              flex flex-col sm:flex-row 
              items-center justify-between`}
            >
              <div className='justify-left w-[100%] mr-2'>
                <label 
                  className="block text-gray-700 text-sm font-bold mb-2" 
                  htmlFor={`startTime-${index}`}
                >
                  Start Time
                </label>
                <input 
                  type="datetime-local"
                  id={`startTime-${index}`}
                  value={timeSlot.startTime}
                  min={minDateTime}
                  onChange={(e) => 
                    handleTimeSlotChange(index, 'startTime', e.target.value)}
                  className={`
                    shadow appearance-none border rounded w-full py-2 px-3 
                    text-gray-700 leading-tight focus:outline-none 
                    focus:shadow-outline`}
                />
              </div>
              <div className="justify-left w-[100%] ">
                <label 
                  className="block text-gray-700 text-sm font-bold mb-2 mt-2 sm:mt-0" 
                  htmlFor={`endTime-${index}`}
                >
                  End Time
                </label>
                <input 
                  type="datetime-local"
                  id={`endTime-${index}`}
                  value={timeSlot.endTime}
                  min={minDateTime}
                  onChange={(e) => handleTimeSlotChange(index, 'endTime', e.target.value)}
                  className={`
                    shadow appearance-none border rounded w-full py-2 px-3 
                    text-gray-700 leading-tight focus:outline-none 
                    focus:shadow-outline`}
                />
              </div>
              <button 
                type="button"
                onClick={() => handleRemoveTimeSlot(index)} 
                className="ml-2 text-red-500 hover:text-red-700 text-[25px]"
              >
                <MdDelete />
              </button>
            </div>
          </div>
        ))}
        <div className="flex flex-col items-center justify-between sm:flex-row">
          <button 
            type="button"
            onClick={handleAddTimeSlot}
            className={`
              w-[100%] bg-blue-500 hover:bg-blue-700 text-white 
              font-bold py-2 px-4 mb-2 mr-2 rounded focus:outline-none 
              focus:shadow-outline`}
          >
            <MdAdd className="inline-block mr-1"/> Add Time Slot
          </button>
          <button 
            type="submit" 
            className={`
              w-[100%] bg-green-500 hover:bg-green-700 text-white 
              font-bold py-2 px-4 mb-2 mr-2 sm:mr-0 rounded 
              focus:outline-none focus:shadow-outline`}
          >
            Create Meeting
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateMeeting;
