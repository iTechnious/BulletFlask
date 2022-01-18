import React, { useEffect, useState } from 'react';
import Thread from '../thread/Thread';
import Category from '../category/Category';
import { Grid } from '@mui/material';

const Content = ({ data, renew }) => {
    const [threads, setThreads] = useState([]);
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        let threadElements = [];
        let categoryElements = [];

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
        });

        setThreads(threadElements);
        setCategories(categoryElements);
    }, [data])

    return (
        <div id={"forum-content"}>
            {/*<Typography variant="h5" sx={{ margin: '30px 0 30px 0' }}>{t("CATEGORIES")}</Typography> */}

            <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
            {
                categories.map((element, index) => {
                    return(<Category key={ index } data={ element } renew={ renew }/>)
                })
            }
            </Grid>

            {/*<Typography variant="h5" sx={{ margin: '30px 0 30px 0' }}>{t("THREADS")}</Typography> */}

            {
                // Render all threads.
                threads.map((element, index) => { return(<Thread key={ index } data={ element } renew={ renew }/>) })
            }
        </div>
    );
}

export default Content;
