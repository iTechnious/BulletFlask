
import React, { useContext } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import { UserContext } from './context/UserContext';
import Login from './pages/Login';
import Forum from './pages/Forum';
import Register from './pages/Register';

const Router = () => {
    // Get user-specific states from global user context.
    const { loggedIn, pending } = useContext(UserContext);
    
    if (pending) return null;

    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/forum"
                    exact
                    element={ loggedIn ? <Forum /> : <Navigate replace to="/login" /> }
                />
                
                <Route
                    path="/login"
                    exact
                    element={ loggedIn ? <Navigate replace to="/forum" /> : <Login /> }
                />
                
                <Route
                    path="/register"
                    exact
                    element={ loggedIn ? <Navigate replace to="/forum" /> : <Register /> }
                />

                <Route
                    path="/"
                    exact
                    element={ loggedIn ? <Navigate replace to="/forum" /> : <Navigate replace to="/login" /> }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;