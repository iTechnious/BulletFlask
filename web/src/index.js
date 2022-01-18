import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import "./index.css";
import "./css/Forum.css";
import { UserProvider } from './context/UserContext';
import Router from './Router';
import { Suspense } from 'react';
import './i18n';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";

export const ColorModeContext = React.createContext("dark");


const App = () => {
    const [colorMode, setColorMode] = useState("dark");

    const scheme = createTheme({
        palette: {
            primary: {main: "#004BA8", light: "#54A1FF", dark: "#002654"},
            secondary: {main: "#FE7F2D", light: "#FEC097", dark: "#963C01"},
            mode: colorMode,
        }
    });

    return(
        <UserProvider>
            <ThemeProvider theme={scheme} >
                <CssBaseline />
                <ColorModeContext.Provider value={{colorMode, setColorMode}}>
                    <Router />
                </ColorModeContext.Provider>
            </ThemeProvider>
        </UserProvider>
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