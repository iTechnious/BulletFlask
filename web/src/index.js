import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import "./index.css";
import { UserProvider } from './context/UserContext';
import Router from './Router';
import { Suspense } from 'react';

import './i18n';


ReactDOM.render(
  <React.StrictMode>
      <Suspense fallback={<span>Loading...</span>}>
          <UserProvider>
            <Router />
          </UserProvider>
      </Suspense>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
