import React from 'react';

export default function Login({ email, setEmail, password, setPassword, errorMessage, handleLogin }) {
  return (
    <div>
      <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Sign In</button>
      {errorMessage && <p>{errorMessage}</p>}
    </div>
  );
}
