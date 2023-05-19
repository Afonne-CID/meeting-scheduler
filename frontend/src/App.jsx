import { 
  BrowserRouter as Router, 
  Routes, 
  Route 
} from 'react-router-dom';
import {
  Login,
  Register,
  MeetingPage,
  PrivateRoute,
  CreateMeeting,
  UpdateMeeting,
  Dashboard,
  NotFound,
} from './components';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route 
          path="/dashboard" 
          element={<PrivateRoute><Dashboard /></PrivateRoute>} 
        />
        <Route 
          path="/create-meeting" 
          element={<PrivateRoute><CreateMeeting /></PrivateRoute>} 
        />
        <Route 
          path="/meetings/:meeting_id" 
          element={<PrivateRoute><MeetingPage /></PrivateRoute>} 
        />
        <Route 
          path="/update-meeting/:meeting_id" 
          element={<PrivateRoute><UpdateMeeting /></PrivateRoute>} 
        />
        <Route path="/" element={<Login />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
