import React, { useState, useEffect, useRef } from 'react';

const ServerImage = () => {
  const [imageSrc, setImageSrc] = useState(null);
  const [error, setError] = useState(null);
  const newImage = useRef(new Image());

  useEffect(() => {
    fetchImage();
    const interval = setInterval(fetchImage, 1000);  // Fetch a new image every second

    // Clean up the interval on unmount
    return () => clearInterval(interval);
  }, []);

  const fetchImage = async () => {
    try {
      const response = await fetch(`${process.env.URL}/api/image`);
      if (!response.ok) {
        throw new Error(response.statusText);
      }

      const blob = await response.blob();
      const newImageSrc = URL.createObjectURL(blob);
      newImage.current.src = newImageSrc;

      newImage.current.onload = () => {
        URL.revokeObjectURL(imageSrc);  // Clean up the old image URL
        setImageSrc(newImageSrc);
        setError(null);
      };
    } catch (e) {
      setError(e.message);
      console.error('Failed to fetch image:', e);
    }
  };

  if (error) {
    return <div>Error loading image: {error}</div>;
  }

  return imageSrc ? <img src={imageSrc} alt="From server" /> : <div>Loading...</div>;
};

export default ServerImage;
