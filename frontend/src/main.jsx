import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import store from './store';
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import PersonalPage from "./pages/PersonalPage";
import ProtectedRoutes from "./components/common/ProtectedRoutes.jsx";
import MainLayout from "./components/common/MainLayout.jsx";

import './index.css'

const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/login",
        element: <LoginPage />,
      },
      {
        element: <ProtectedRoutes />,
        children: [
          {
            path: "/me",
            element: <PersonalPage />,
          }
        ]
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <RouterProvider router={router} />
  </Provider>,
)
