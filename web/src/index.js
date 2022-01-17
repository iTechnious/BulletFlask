import React from 'react';
import ReactDOM from 'react-dom';
import "./index.css";
import "./css/Forum.css";
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