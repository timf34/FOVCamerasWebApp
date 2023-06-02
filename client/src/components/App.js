import React, { useState } from 'react';
import Login from './Login';
import StatusList from './StatusList';
import useStatus from './useStatus';
import useAuth from './useAuth';
import CommandButton from './useSendCommand';
import ServerImage from './ServerImage';

export default function App() {
  const [useFirebase, setUseFirebase] = useState(false);  // set to true to use firebase database listening, false to use websocket listening

  const status = useStatus(useFirebase);
  const { user, email, setEmail, password, setPassword, errorMessage, handleLogin } = useAuth();

  console.log("status:", status);

  return (
    <div className="App">
      {!user ? (
        <Login email={email} setEmail={setEmail} password={password} setPassword={setPassword} errorMessage={errorMessage} handleLogin={handleLogin} />
      ) : (
        <div>
          <StatusList status={status} />
          <CommandButton />
          <ServerImage />
        </div>
      )}
    </div>
  );
}
