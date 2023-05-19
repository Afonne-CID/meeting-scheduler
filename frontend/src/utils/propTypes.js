import PropTypes from 'prop-types';

export const meetingShape = PropTypes.shape({
  id: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  timeslots: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    start_time: PropTypes.string.isRequired,
    end_time: PropTypes.string.isRequired,
    votes: PropTypes.arrayOf(PropTypes.shape({
      user_id: PropTypes.number.isRequired,
    })),
    user_id: PropTypes.number.isRequired,
  })),
});

export const timeSlotShape = PropTypes.shape({
  id: PropTypes.number.isRequired,
  start_time: PropTypes.string.isRequired,
  end_time: PropTypes.string.isRequired,
  votes: PropTypes.arrayOf(PropTypes.shape({
    user_id: PropTypes.number.isRequired,
  })),
  user_id: PropTypes.number.isRequired,
});

export const userShape = PropTypes.shape({
  id: PropTypes.number,
});

export const funcType = PropTypes.func;
export const nodeType = PropTypes.node;
export const stringType = PropTypes.string;
