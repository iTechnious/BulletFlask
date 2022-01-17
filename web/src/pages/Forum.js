import React, { useEffect, useState } from 'react';
import { Container } from '@mui/material';
import Current from '../components/content/Current';
import Content from '../components/content/Content';
import '../css/Forum.css';
import Navbar from '../components/navbar/Navbar';
import Breadcrumb from "../components/breadcrumb/Breadcrumb";

const Forum = () => {
    // Info about the current element.
    const [current, setCurrent] = useState(null);
    // Content of the current element.
    const [content, setContent] = useState(null);
    // Breadcrumb data.
    const [breadcrumb, setBreadcrumb] = useState([]);
    // Loading state.
    const [loading, setLoading] = useState(true);


    const getData = (location) => {
        setLoading(true);
        location = location.toString();
        
        fetch('/api/content/get/?location=' + location, {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setCurrent(data['current']);
            setContent(data['contents']);
            setLoading(false);
        })
        .catch(console.log);

        fetch('/api/content/breadcrumb/?location=' + location, {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setBreadcrumb(data)
        })
    }

    useEffect(() => {
        getData(0);
    // eslint-disable-next-line
    }, []);

    if (current === null || content === null) return <Navbar IsLoading={true} />;

    return (
        <>
            <Navbar IsLoading={loading} />
            <Breadcrumb data={ breadcrumb } renew={ getData } />
            <Container>
                <Current data={ current } />
                <Content data={ content } renew={ getData } />
            </Container>
        </>
    );
}

export default Forum;