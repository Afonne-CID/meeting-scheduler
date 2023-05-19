import { useSelector } from 'react-redux';

const StatusMessage = () => {
  const authError = useSelector(state => state.auth.error);
  const meetingError = useSelector(state => state.meeting.error);
  const authSuccess = useSelector(state => state.auth.success)
  const meetingSuccess = useSelector(state => state.meeting.success)

  // Define classes for error and success messages
  const baseClasses = `font-bold py-2 px-4 rounded 
                      focus:outline-none focus:shadow-outline
                      `;
  const errorClasses = `${baseClasses} bg-red-500`;
  const successClasses = `${baseClasses} bg-green-500`;

  // Determine if there are any error messages
  const isError = authError || meetingError;
  const isSuccess = authSuccess || meetingSuccess;

  // Construct the error or success message
  const errorMessage = authError || meetingError;
  const successMessage = authSuccess || meetingSuccess;

  return (
    <div className={`${(isError || isSuccess) ? 'flex' : 'hidden'}`}>
      {isError && <div className={errorClasses}>{errorMessage}</div>}
      {isSuccess && <div className={successClasses}>{successMessage}</div>}
    </div>
  );
};

export default StatusMessage;
