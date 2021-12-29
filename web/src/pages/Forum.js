import React, { useEffect, useState } from 'react';
import { Container } from '@mui/material';
import Current from '../components/content/Current';
import Content from '../components/content/Content';
import '../css/Forum.css';
import Navbar from '../components/navbar/Navbar';

const Forum = () => {
    // Info about the current element.
    const [current, setCurrent] = useState(null);
    // Content of the current element.
    const [content, setContent] = useState(null);

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
        getData(0);
    // eslint-disable-next-line
    }, []);

    if (current === null || content === null) return null;

    return (
        <>
            <Navbar />
            <Container>
                <Current data={ current } />
                <Content data={ content } />
            </Container>
        </>
    );
}

export default Forum;