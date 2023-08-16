import React, {useState, useEffect, useRef, useContext} from 'react';
import {TransformWrapper, TransformComponent} from "react-zoom-pan-pinch";
import StreamContext from './StreamContext';

const ServerImage = () => {
    const [imageSrc, setImageSrc] = useState(null);
    const [error, setError] = useState(null);
    const newImage = useRef(new Image());
    const {isStreaming} = useContext(StreamContext);

    useEffect(() => {
        fetchImage();
        const interval = setInterval(fetchImage, 500);

        // Clean up the interval on unmount
        return () => clearInterval(interval);
    }, [isStreaming]);

    const fetchImage = async () => {
        if (!isStreaming) {
            // If the streaming is stopped, we don't try to fetch the image
            setImageSrc(null); // clear the image when stream is stopped
            return;
        }
        try {
            console.log("REACT_APP_URL: " + process.env.REACT_APP_URL);
            const response = await fetch(`${process.env.REACT_APP_URL}/api/image`);
            if (response.status === 404) {
                throw new Error("Image not found. Please check if the camera is working properly.");
            } else if (response.status >= 500) {
                throw new Error("Server error. Please try again later.");
            } else  if (!response.ok) {
                throw new Error("Unexpected error. Please refresh the page and try again.");
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
                {imageSrc ? <img src={imageSrc} alt="From server" /> : <div>No stream to show...</div>}
                {error && <div className="error-popup">Error loading image: {error}</div>}
            </TransformComponent>
        </TransformWrapper>
    );
};

export default ServerImage;
