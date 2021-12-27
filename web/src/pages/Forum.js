import React, { useEffect, useState } from 'react';
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

        fetch('/api/content/get/?location=' + location)
            .then(res => res.json())
            .then(data => {
                setCurrent(data['current']);
                setContent(data['contents']);
            })
            .catch(console.log);
    } 

    useEffect(() => getData(0), []);

    if (current === null || content === null) return null;

    return (
        <>
            <main>
                <Current data={ current } />
                <Content data={ content } />
            </main>
            <Footer />
        </>
    );
}

export default Forum;