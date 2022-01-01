import React, { useEffect, useState } from 'react';
import Thread from '../thread/Thread';
import Category from '../category/Category';
import { Grid, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';

const Content = ({ data }) => {
    const [threads, setThreads] = useState([]);
    const [categories, setCategories] = useState([]);

    const { t } = useTranslation();

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

            // Update states with the processed elements.
            setThreads(threadElements);
            setCategories(categoryElements);
        });
    // eslint-disable-next-line
    }, []);

    return (
        <>
        <Typography variant="h5" sx={{ margin: '30px 0 30px 0' }}>{t("CATEGORIES")}</Typography>
        
        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                {
                    // Render all categories.
                    categories.map((element, index) => (<Category key={ index } data={ element } />))
                }
        </Grid>

        <Typography variant="h5" sx={{ margin: '30px 0 30px 0' }}>{t("THREADS")}</Typography>

        {
            // Render all threads.
            threads.map((element, index) => (<Thread key={ index } data={ element } />))
        }
        </>
    );
}

export default Content;
