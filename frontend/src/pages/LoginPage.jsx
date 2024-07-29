import { useState } from 'react';
import { Button, Input } from "antd";
import { useNavigate } from 'react-router-dom';
import { useDispatch } from "react-redux";

import { useLoginMutation } from '../api/authApi';
import { setCredentials } from "../slices/authSlice";

const LoginPage = () => {
  const [login, { isLoading, error }] = useLoginMutation();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { access_token, refresh_token } = await login({ username, password }).unwrap();
      dispatch(setCredentials({ token: access_token, refreshToken: refresh_token }));
      navigate('/me');
    } catch (err) {
      console.error('Failed to login:', err);
    }
  };

  return (
    <div>
      <h2>Sign in</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <Input.Password
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button htmlType="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </Button>
      </form>
      {error && <p>Error: {error.data?.message || 'Failed to login'}</p>}
    </div>
  );
};

export default LoginPage;