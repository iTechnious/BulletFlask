import React, { useEffect, useState } from 'react';
import { Container } from '@mui/material';
import Current from '../components/content/Current';
import Content from '../components/content/Content';
import Footer from '../components/footer/Footer';
import '../css/Forum.css';

const Forum = () => {
    // Info about the current element.
    const [current, setCurrent] = useState(null);
    // Content of the current element.
    const [content, setContent] = useState(null);

    const getData = (location) => {
        location = location.toString();

        var formData = new FormData();

        fetch('/login/', {
            method: 'POST',
            credentials: 'include'
        })
            .then(res => {
                if (res.status === 200) {
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
            })


    } 

    useEffect(() => getData(0), []);

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