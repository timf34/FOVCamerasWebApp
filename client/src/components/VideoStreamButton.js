import React, { useState } from 'react';
import ReactPlayer from 'react-player';

function VideoStreamButton() {
  const [streamUrl, setStreamUrl] = useState(null);

  return (
    <div>
      <button onClick={() => setStreamUrl('http://localhost:5000/api/video')}>Start Streaming</button>
      {streamUrl && <ReactPlayer url={streamUrl} playing controls />}
    </div>
  );
}

export default VideoStreamButton;
