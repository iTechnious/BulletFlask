import React from 'react';
import ReactDOM from 'react-dom';
import Forum from './pages/Forum';
import reportWebVitals from './reportWebVitals';
import "./index.css";
import { UserProvider } from './context/UserContext';

ReactDOM.render(
  <React.StrictMode>
      <UserProvider>
        <Forum />
      </UserProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
