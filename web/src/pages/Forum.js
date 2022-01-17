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
    // For loader delay
    const timerRef = React.useRef();


    const getData = (location) => {
        if (timerRef.current) {
          clearTimeout(timerRef.current);
        }
        setLoading(true);
        location = location.toString();
        
        fetch('/api/content/get/?location=' + location, {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setCurrent(data['current']);
            setContent(data['contents']);
            timerRef.current = window.setTimeout(() => {
              setLoading(false);
            }, 200);
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

    return (
        <>
            <Navbar IsLoading={loading} />
            {breadcrumb !== null ? <Breadcrumb data={breadcrumb} renew={getData}/> : null}
            <Container>
                {current !== null ? <Current data={current}/> : null}
                {content !== null ? <Content data={content} renew={getData}/> : null}
            </Container>
        </>
    );
}

export default Forum;