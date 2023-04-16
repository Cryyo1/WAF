import './App.css';
import React from 'react';
import Main from './components/Main/Main';
import Login from './components/Login/Login';
import DetailedReq from './components/DetailedReq/DetailedReq';
import { Routes, Route, Outlet, Navigate } from 'react-router-dom';
import injectContext from "./store/appContext";
import { Context } from "./store/appContext";
function App() {
  const { actions } = React.useContext(Context);
  const GuestRoute = () => {
    return !actions.isAuthenticated() ? (<Outlet />) : (<Navigate to="/" replace />);
  };
  const ProtectedRoutes = () => {
    return actions.isAuthenticated() ? (<Outlet />) : (<Navigate to="/login" replace />);
  };

  if (!actions.isAuthenticated) {
    return <h1>Loading...</h1>;
  }
  return (
    <Routes>
      <Route element={<GuestRoute />}>
        <Route path="/login" element={<Login />} />
      </Route>

      <Route element={<ProtectedRoutes />}>
        <Route path="/" element={<Navigate to="/home" replace />} />
        <Route path="/home" element={<Main />} />
        <Route path="/request" element={<DetailedReq />} />
        <Route path="*" element={<div>404 path not found </div>} />
      </Route>
    </Routes>
  );
}

export default injectContext(App);
