import React, {useContext, useEffect, useState} from 'react';
import {Container, Fade} from '@mui/material';
import Current from '../components/forum_content/Current';
import Content from '../components/forum_content/Content';
import '../css/Forum.css';
import Navbar from '../components/navbar/Navbar';
import Breadcrumb from "../components/misc/Breadcrumb";
import Error from "../components/navbar/Error";
import {UserContext} from "../index";
import Login from "./Login";
import { useParams } from "react-router-dom";
import Box from "@mui/material/Box";
import ForumActionSD from "../components/misc/ForumActionsSD";

export const LocationContext = React.createContext();

const Forum = () => {
    const { preDefLocation, preDefVersion } = useParams();
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
        
        fetch('/api/content/get/?location=' + location + (preDefVersion !== undefined ? "&version="+preDefVersion : ""), {
            credentials: 'include'
        })
        .then(res => res.json())
        .then(data => {
            setCurrent(data['current']);
            setContent(data['contents']);
            timerRef.current = window.setTimeout(() => {
              setLoading(false);
            }, 90);
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
        window.scrollTo({
            top: 0
        });
        if (loggedIn) {
            if (preDefLocation !== undefined) {getData(preDefLocation, preDefVersion)} else {
                getData(window.location.href.substring(window.location.href.lastIndexOf('/') + 1))
            }
        } else {
            timerRef.current = window.setTimeout(() => {
              setLoading(false);
            }, 200);
        }
    }, [loggedIn, preDefLocation, preDefVersion]);

    if (pending) { return null; }
    if (!loggedIn) { return <Login /> }
    return (
        <>
            <LocationContext.Provider value={{preDefLocation, preDefVersion}}>
                <Box style={{position: "sticky", top: 0}}>
                    <Navbar IsLoading={loading} />
                    {breadcrumb !== null ? <Breadcrumb data={breadcrumb} renew={getData}/> : null}
                </Box>

                <Error message={loadError["message"]} setMessage={setLoadError} severity={loadError["severity"]} />

                <ForumActionSD />

                <Fade id={"forum-root"} in={!loading} timeout={{enter: 200, exit: 70}} appear>
                    <Container style={ {padding: 0} }>
                        {current !== undefined ? <Current data={current}/> : null}
                        {content !== undefined ? <Content data={content} renew={getData}/> : null}
                    </Container>
                </Fade>
            </LocationContext.Provider>
        </>
    );
}

export default Forum;