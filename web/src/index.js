import React, {useEffect, useState} from 'react';
import ReactDOM from 'react-dom';
import "./index.css";
import "./css/Forum.css";
import Router from './Router';
import { Suspense } from 'react';
import './i18n';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";

export const ColorModeContext = React.createContext("dark");
export const UserContext = React.createContext();

const App = () => {
    // Whether or not the user is logged in.
    const [loggedIn, setLoggedIn] = useState(false);
    // Whether or not the login request is already done.
    const [pending, setPending] = useState(false);
    // User object returned by the /login/ API.
    const [user, setUser] = useState({});

    const checkLogin = () => {
        setPending(true);

        fetch('/login/', {
            method: 'POST',
            credentials: 'include'
        })
            .then(res => {
                if (res.status === 200 || res.status === 202) {
                    setLoggedIn(true);
                    // Parse response and save user object in state.
                    res.json().then(res => setUser(res.user));
                    setPending(false);
                } else {
                    setLoggedIn(false);
                    setPending(false);
                }

                setPending(false);
            });
    }
    useEffect(checkLogin, []);

    const [colorMode, setColorMode] = useState("dark");
    const scheme = createTheme({
        palette: {
            primary: {main: "#004BA8", light: "#54A1FF", dark: "#002654"},
            secondary: {main: "#FE7F2D", light: "#FEC097", dark: "#963C01"},
            mode: colorMode,
        }
    });

    return(
        <UserContext.Provider
            value={{
                loggedIn,
                setLoggedIn,
                pending,
                setPending,
                user,
                setUser,
                checkLogin
            }}>
            <ThemeProvider theme={scheme} >
                <CssBaseline />
                <ColorModeContext.Provider value={{colorMode, setColorMode}}>
                    <Router />
                </ColorModeContext.Provider>
            </ThemeProvider>
        </UserContext.Provider>
    );
}


ReactDOM.render(
  <React.StrictMode>
      <Suspense fallback={<span>Loading...</span>}>
          <App />
      </Suspense>
  </React.StrictMode>,
  document.getElementById('root')
);