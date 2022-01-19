import React, {useContext, useEffect, useState} from 'react';
import { Container, Fade } from '@mui/material';
import Current from '../components/content/Current';
import Content from '../components/content/Content';
import '../css/Forum.css';
import Navbar from '../components/navbar/Navbar';
import Breadcrumb from "../components/breadcrumb/Breadcrumb";
import Error from "../components/Error";
import {UserContext} from "../index";
import Login from "./Login";
import { useParams } from "react-router-dom";

const Forum = () => {
    const { preDefLocation } = useParams();
    // Info about the current element.
    const [current, setCurrent] = useState(undefined);
    // Content of the current element.
    const [content, setContent] = useState(undefined);
    // Breadcrumb data.
    const [breadcrumb, setBreadcrumb] = useState([]);
    // Loading state.
    const [loading, setLoading] = useState(true);
    const [loadError, setLoadError] = useState({});
    // For loader delay
    const timerRef = React.useRef(0);

    const {loggedIn, pending} = useContext(UserContext);


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
        .catch(e => {
            setLoadError({"message": e.message, "severity": "error"});
        });

        fetch('/api/content/breadcrumb/?location=' + location, {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setBreadcrumb(data)
        })
        .catch(e => {
            setLoadError({"message": e.message, "severity": "error"});
        });
    }

    useEffect(() => {
        if (loggedIn) {
            if (preDefLocation !== undefined) {getData(preDefLocation)} else {
                getData(window.location.href.substring(window.location.href.lastIndexOf('/') + 1))
            }
        } else {
            timerRef.current = window.setTimeout(() => {
              setLoading(false);
            }, 200);
        }
    // eslint-disable-next-line
    }, [loggedIn, preDefLocation]);

    if (pending) { return null; }
    if (!loggedIn) { return <Login /> }
    return (
        <>
            <Navbar IsLoading={loading} />
            <Error message={loadError["message"]} setMessage={setLoadError} severity={loadError["severity"]} />

            {breadcrumb !== null ? <Breadcrumb data={breadcrumb} renew={getData}/> : null}

            <Fade id={"forum-root"} in={!loading} timeout={{enter: 200, exit: 70}} appear>
                <Container style={ {padding: 0} }>
                    {current !== undefined ? <Current data={current}/> : null}
                    {content !== undefined ? <Content data={content} renew={getData}/> : null}
                </Container>
            </Fade>

        </>
    );
}

export default Forum;