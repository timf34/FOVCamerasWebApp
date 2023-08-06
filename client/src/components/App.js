import React, { useState } from 'react';
import StatusList from './StatusList';
import useStatus from './useStatus';
import CommandButton from './useSendCommand';
import ServerImage from './ServerImage';
import MotorControlForm from './MotorControlForm';
import StartCameraControlButton from './StartStopCameraControl';
import CameraStreamForm from './StartStopCameraStream';
import MotorPositions from './MotorPositions';
import DeviceSelection from "./DeviceSelection";
import RecordVideoForm from './StartStopRecordVideo';
import SyncS3Form from "./StartStopS3Sync"
import { StreamProvider } from './StreamContext';
import '../stylesheets/App.css'

export default function App() {
  const [useFirebase, setUseFirebase] = useState(false);  // set to true to use firebase database listening, false to use websocket listening
  const [isStreaming, setStreaming] = useState(false);

  const status = useStatus(useFirebase);

  return (
      <div className="App">
        <div>
          <div className='component-container'>
            <h3><u>Device Diagnostics</u></h3>
          </div>

          <div className="component-container">
            <StatusList status={status} />
          </div>

          <div className="component-container">
            <CommandButton />
          </div>

          <div className='component-container'>
            <h3><u>Device Selection</u></h3>
          </div>

          <div className="component-container">
            <DeviceSelection />
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
            <h3><u>Record Video</u></h3>
          </div>

          <div className='component-container'>
            <RecordVideoForm />
          </div>

          <div className='component-container'>
            <h3><u>S3 Sync</u></h3>
          </div>

          <div className='component-container'>
            <SyncS3Form />
          </div>
        </div>
      </div>
  );
}
