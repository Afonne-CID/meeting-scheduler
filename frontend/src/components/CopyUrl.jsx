import { FaCopy, FaCheck } from 'react-icons/fa';
import { useState } from 'react';
import { stringType } from '../utils/propTypes';

const CopyUrl = ({ meetingUrl }) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(meetingUrl);
    setIsCopied(true);
  };

  return (
    <p className='m-2 p-2 bg-blue-100 rounded px-2'> 
      {meetingUrl}
      <button 
        onClick={handleCopy} 
        className="ml-2 text-blue-600 hover:text-blue-800"
      >
        {isCopied ? <FaCheck /> : <FaCopy />}
      </button>
    </p>
  );
};

CopyUrl.propTypes = {
  meetingUrl: stringType.isRequired,
};

export default CopyUrl;