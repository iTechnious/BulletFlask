import {Card, CardContent, Grid, Typography} from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';

const Thread = ({ data }) => {
    const { t } = useTranslation();

    return (
        <Grid item>
            <NavLink to={"/forum/"+data.id} style={{textDecoration: "none"}}>
                <Card className="thread" sx={{ padding: '10px'}} style={ {cursor: "pointer"} }>
                    <CardContent>
                        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                            { t('THREAD') }
                        </Typography>

                        <Typography variant="h5">{ data.name }</Typography>
                    </CardContent>
                </Card>
            </NavLink>
        </Grid>


    );
}

export default Thread;