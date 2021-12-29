
import React, { createContext, useEffect, useState } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    // Whether or not the user is logged in.
    const [loggedIn, setLoggedIn] = useState(false);
    // Whether or not the login request is already done.
    const [pending, setPending] = useState(false);
    // User object returned by the /login/ API.
    const [user, setUser] = useState({});

    // Check if user is already logged in.
    useEffect(() => {
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

    // eslint-disable-next-line
    }, []);

    return (
        <UserContext.Provider
            value={{
                loggedIn,
                setLoggedIn,
                pending,
                setPending,
                user,
                setUser
            }}
        >
            { children }
        </UserContext.Provider>
    );
}