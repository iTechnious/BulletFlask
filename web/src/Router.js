import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Forum from './pages/Forum';
import Register from './pages/Register';

const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/forum/:preDefLocation"
                    exact
                    element={ <Forum /> }
                />
                <Route
                    path="/forum/:preDefLocation/:preDefVersion"
                    exact
                    element={ <Forum /> }
                />
                <Route
                    path="/forum"
                    exact
                    element={ <Navigate replace to="/forum/0" /> }
                />
                <Route
                    path="/login"
                    exact
                    element= { <Login /> }
                />
                
                <Route
                    path="/register"
                    exact
                    element={ <Register /> }
                />

                <Route
                    path="/"
                    exact
                    element={ <Navigate replace to="/forum/0" /> }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;