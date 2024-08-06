import { Layout, Menu } from 'antd';
import { Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth.js";
import { useDispatch } from "react-redux";
import { logout } from "../../slices/authSlice.js";

import PDPImage from '../../assets/pdp.png';

const { Header, Content, Footer } = Layout;


const MainLayout = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const getHeaderItems = () => isAuthenticated ? [
    {
      key: "home",
      label: "Home",
      onClick: () => navigate('/'),
    },
    {
      key: 'plan',
      label: 'Plan',
      onClick: () => navigate('/me'),
    },
    {
      key: 'logout',
      label: 'Logout',
      onClick: () => dispatch(logout()),
    },
  ] : [
    {
      key: "home",
      label: "Home",
      onClick: () => navigate('/'),
    },
    {
      key: 'login',
      label: 'Sign in',
      onClick: () => navigate('/login'),
    }
  ]

  return (
    <Layout>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center'
        }}
      >
        <div
          style={{
            height: "100%",
            display: "flex",
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#f5f5f5',
            marginRight: '2rem',
            cursor: 'pointer'
          }}
          onClick={() => navigate('/')}
        >
          <img src={PDPImage} alt="app logo" />
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          items={getHeaderItems()}
          style={{
            flex: 1,
            minWidth: 0,
          }}
        />
      </Header>
      <Content
        style={{
          padding: '0 48px',
        }}
      >
        <Outlet />
      </Content>
      <Footer
        style={{
          textAlign: 'center',
        }}
      >
        PDP ©{new Date().getFullYear()}
      </Footer>
    </Layout>
  );
};

export default MainLayout;