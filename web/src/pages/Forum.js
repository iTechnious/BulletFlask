import React, { useContext, useEffect, useState } from 'react';
import { Container } from '@mui/material';
import Current from '../components/content/Current';
import Content from '../components/content/Content';
import Footer from '../components/footer/Footer';
import '../css/Forum.css';
import { UserContext } from '../context/UserContext';

const Forum = () => {
    // Info about the current element.
    const [current, setCurrent] = useState(null);
    // Content of the current element.
    const [content, setContent] = useState(null);

    // Grab user states from global states.
    const { loggedIn, pending, setLoggedIn, setPending } = useContext(UserContext);

    const getData = (location) => {
        location = location.toString();
        
        fetch('/api/content/get/?location=' + location, {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setCurrent(data['current']);
            setContent(data['contents']);
        })
        .catch(console.log);
    } 

    useEffect(() => {
        // Login (check) is still pending.
        if (pending) return;
        
        // User not logged in.
        if (!loggedIn) {
            var formData = new FormData();  
            formData.append('email', 'fabian@fabiancdng.com');
            formData.append('password', 'tester');  
            
            // TODO: Remove hard-coded login request and replace with login form.
            fetch('/login/', {
                method: 'POST',
                credentials: 'include',
                body: formData
            })
            .then(res => {
                if (res.status === 200) setLoggedIn(true);
                else setLoggedIn(false);
                setPending(false);
                getData(0);
            });
        } else {
            // Logged in; get data.
            getData(0);
        }
    // eslint-disable-next-line
    }, [loggedIn, pending]);

    if (current === null || content === null) return null;

    return (
        <>
            <Container>
                <Current data={ current } />
                <Content data={ content } />
            </Container>
            <Footer />
        </>
    );
}

export default Forum;