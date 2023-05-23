import { useState, useEffect } from 'react';
import { signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { auth } from './firebase';

export default function useAuth() {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
  }, []);

  const handleLogin = async () => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      setErrorMessage(null);
    } catch (error) {
      console.error('Failed to sign in:', error);
      setErrorMessage('Failed to sign in');
    }
  };

  return { user, email, setEmail, password, setPassword, errorMessage, handleLogin };
}
