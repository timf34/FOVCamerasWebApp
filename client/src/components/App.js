import React, { useState } from 'react';
import Login from './Login';
import StatusList from './StatusList';
import useStatus from './useStatus';
import useAuth from './useAuth';
import CommandButton from './useSendCommand';
import ServerImage from './ServerImage';
import MotorControlForm from './MotorControlForm';
import StartCameraControlButton from './StartStopCameraControl';
import CameraStreamForm from './StartStopCameraStream';
import MotorPositions from './MotorPositions';
import RecordVideoForm from './StartStopRecordVideoScript';
import { StreamProvider } from './StreamContext';
import '../stylesheets/App.css'

export default function App() {
  const [useFirebase, setUseFirebase] = useState(false);  // set to true to use firebase database listening, false to use websocket listening
  const [isStreaming, setStreaming] = useState(false);

  const status = useStatus(useFirebase);
  const { user, email, setEmail, password, setPassword, errorMessage, handleLogin } = useAuth();

  console.log("status:", status);

  return (
    <div className="App">
      {!user ? (
        <Login email={email} setEmail={setEmail} password={password} setPassword={setPassword} errorMessage={errorMessage} handleLogin={handleLogin} />
      ) : (
        <div>
          <div className='component-container'>
            <h3><u>Device Diagnostics</u></h3>
          </div>

          <div className="component-container">
            <StatusList status={status} />
          </div>

          <div className="component-container">
            <CommandButton />
          {/*  Note that this doens't work rn...*/}
          </div>

          <div className='component-container'>
            <h3><u>Camera Streaming</u></h3>
          </div>

          <StreamProvider value={{ isStreaming, setStreaming }}>
            <div className="component-container">
              <CameraStreamForm />
            </div>

            <div className="component-container">
              <ServerImage />
            </div>
          </StreamProvider>

          <div className='component-container'>
            <h3><u>Motor Control</u></h3>
          </div>

          <div className="component-container">
            <StartCameraControlButton />
          </div>

          <div className="component-container">
            <MotorControlForm />
          </div>

          <div className='component-container'>
            <MotorPositions />
          </div>

          <div className='component-container'>
            <h3><u>Record Video Script</u></h3>
          </div>

          <div className='component-container'>
            <RecordVideoForm />
          </div>

        </div>
      )}
    </div>
  );
}
