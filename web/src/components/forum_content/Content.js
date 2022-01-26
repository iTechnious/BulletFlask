import React, { useEffect, useState } from 'react';
import Thread from '../forum_types/Thread';
import Category from '../forum_types/Category';
import Comment from '../forum_types/Comment';
import {Divider, Grid} from '@mui/material';
import {useTranslation} from "react-i18next";

const Content = ({ data, renew }) => {
    const [threads, setThreads] = useState([]);
    const [categories, setCategories] = useState([]);
    const [comments, setComments] = useState([]);

    const [windowSize, setWindowSize] = useState(window.innerWidth);

    const { t } = useTranslation();

    useEffect(() => {
        window.addEventListener("resize", () => {setWindowSize(window.innerWidth)});

        let threadElements = [];
        let categoryElements = [];
        let commentElements = [];

        // Iterate over each element and append it to the correct array.
        data.forEach(element => {
            // Element is of type thread.
            if (element.type === 'thread') {
                threadElements.push(element);
            }
            // Element is of type category.
            if (element.type === 'category') {
                categoryElements.push(element);
            }
            // Element is of type comment.
            if (element.type === 'comment') {
                commentElements.push(element);
            }
        });

        setThreads(threadElements);
        setCategories(categoryElements);
        setComments(commentElements);
    }, [data])

    return (
        <div id={"forum-content"} style={{ marginBottom: "50px" }}>
            {/* -------------- COMMENTS --------------*/}
            <>
            {
                comments.length !== 0 ? <Divider style={{margin: "10px 0"}}>{t("COMMENTS")}</Divider> : null
            }
            </>
            <Grid container
                  direction={"column"}
                  rowSpacing={1}
                  justifyContent={"center"}>
                {
                    // Render all threads.
                    comments.map((element, index) => { return(<Comment key={ index } data={ element }/>) })
                }
            </Grid>
            {/* -------------- CATEGORIES --------------*/}
            <>
            {
                categories.length !== 0 ? <Divider style={{margin: "10px 0"}}>{t("CATEGORIES")}</Divider> : null
            }
            </>
            <Grid container
                  direction={windowSize < 550 ? "column" : "row"}
                  rowSpacing={2}
                  spacing={{ xs: 2, md: 3 }}
                  columns={{ xs: 4, sm: 8, md: 12 }}
                  justifyContent={"center"}>
            {
                categories.map((element, index) => {
                    return(<Category key={ index } data={ element }/>)
                })
            }
            </Grid>
            {/* -------------- THREADS --------------*/}
            <>
            {
                threads.length !== 0 ? <Divider style={{margin: "10px 0"}}>{t("THREADS")}</Divider> : null
            }
            </>
            <Grid container
                  direction={"column"}
                  rowSpacing={1}
                  justifyContent={"center"}>
                {
                    // Render all threads.
                    threads.map((element, index) => { return(<Thread key={ index } data={ element }/>) })
                }
            </Grid>

        </div>
    );
}

export default Content;
