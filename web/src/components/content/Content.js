import React from 'react';
import Thread from '../thread/Thread';
import Category from '../category/Category';
import { Grid } from '@mui/material';

const Content = ({ data }) => {
    return (
        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                {
                    data.map((element, index) => {
                        element.type === 'category' && <Category key={ index } data={ element } />
                        element.type === 'thread' && <Thread key={ index } data={ element } />
                    })
                }
        </Grid>
    );
}

export default Content;
