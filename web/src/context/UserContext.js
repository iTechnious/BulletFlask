
import React, { createContext, useEffect, useState } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    // Whether or not the user is logged in.
    const [loggedIn, setLoggedIn] = useState(false);
    // Whether or not the login request is already done.
    const [pending, setPending] = useState(true);

    // Check if user is already logged in.
    useEffect(() => {
        // Login data as FormData.
        // var formData = new FormData();

        fetch('/login/', {
            method: 'POST',
            credentials: 'include'
        })
        .then(res => {
            if (res.status === 200) setLoggedIn(true);
            else setLoggedIn(false);

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
                setPending
            }}
        >
            { children }
        </UserContext.Provider>
    );
}