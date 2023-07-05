import { createContext, useState } from 'react';

const DeviceContext = createContext();

export const DeviceProvider = ({ children }) => {
    const [deviceId, setDeviceId] = useState('jetson1');

    return (
        <DeviceContext.Provider value={{ deviceId, setDeviceId }}>
            {children}
        </DeviceContext.Provider>
    );
};

export default DeviceContext;
