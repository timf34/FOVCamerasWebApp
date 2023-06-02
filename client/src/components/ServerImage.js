import React, { useState, useEffect } from 'react';

const ServerImage = () => {
  const [imageSrc, setImageSrc] = useState(null);

  useEffect(() => {
    fetchImage();
    const interval = setInterval(fetchImage, 1000);  // Fetch a new image every second

    // Clean up the interval on unmount
    return () => clearInterval(interval);
  }, []);

  const fetchImage = async () => {
    const response = await fetch('http://localhost:5000/api/image');
    if (!response.ok) {
      console.error('Failed to fetch image:', response.statusText);
      return;
    }

    const blob = await response.blob();
    const imageSrc = URL.createObjectURL(blob);
    setImageSrc(imageSrc);
  };

  if (imageSrc === null) {
    return <div>Loading...</div>;
  }

  return <img src={imageSrc} alt="From server" />;
};

export default ServerImage;
