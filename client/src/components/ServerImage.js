import React, { useState, useEffect, useRef } from 'react';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

const ServerImage = () => {
  const [imageSrc, setImageSrc] = useState(null);
  const [error, setError] = useState(null);
  const newImage = useRef(new Image());

  useEffect(() => {
    fetchImage();
    const interval = setInterval(fetchImage, 200);  // Fetch a new image every 1/3 second

    // Clean up the interval on unmount
    return () => clearInterval(interval);
  }, []);

  const fetchImage = async () => {
    try {
      console.log("REACT_APP_URL: " + process.env.REACT_APP_URL);
      const response = await fetch(`${process.env.REACT_APP_URL}/api/image`);
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

  return (
    <TransformWrapper>
      <TransformComponent>
        {imageSrc ? <img src={imageSrc} alt="From server" /> : <div>Loading...</div>}
      </TransformComponent>
    </TransformWrapper>
  );
};

export default ServerImage;
