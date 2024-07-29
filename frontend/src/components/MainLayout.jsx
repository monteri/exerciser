import { Layout, Menu } from 'antd';
import { Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth.js";
import { useDispatch } from "react-redux";
import { logout } from "../slices/authSlice.js";

const { Header, Content, Footer } = Layout;


const MainLayout = () => {
  const isAuthenticated = useAuth();
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
          alignItems: 'center',
        }}
      >
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['2']}
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