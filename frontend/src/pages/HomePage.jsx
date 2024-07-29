import { useDispatch } from "react-redux";
import { Button } from "antd";

import { logout } from "../slices/authSlice.js";
import {useNavigate} from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  return (
    <div>
      <h1>Welcome to the Home Page</h1>
      <Button onClick={() => navigate('/login')}>Login</Button>
      <Button onClick={() => dispatch(logout())}>Logout</Button>
    </div>
  );
};

export default HomePage;