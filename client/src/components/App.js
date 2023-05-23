import React from 'react';
import Login from './Login';
import StatusList from './StatusList';
import useWebSocketStatus from './useWebSocketStatus';
import useAuth from './useAuth';

export default function App() {
  const status = useWebSocketStatus();
  const { user, email, setEmail, password, setPassword, errorMessage, handleLogin } = useAuth();

  return (
    <div className="App">
      {!user ? (
        <Login email={email} setEmail={setEmail} password={password} setPassword={setPassword} errorMessage={errorMessage} handleLogin={handleLogin} />
      ) : (
        <StatusList status={status} />
      )}
    </div>
  );
}
