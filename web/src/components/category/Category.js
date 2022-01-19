import { Card, CardContent, Grid, Typography } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';
import {NavLink} from "react-router-dom";

const Category = ({ data }) => {
    const { t } = useTranslation();

    return (
        <Grid item xs={6}>
            <NavLink to={"/forum/"+data.id} style={{textDecoration: "none"}}>
                <Card className="category" sx={{ padding: '10px', marginBottom: '20px' }} style={ {cursor: "pointer"} }>
                    <CardContent>
                        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                            { t('CATEGORY') }
                        </Typography>

                        <Typography variant="h5">{ data.name }</Typography>
                    </CardContent>
                </Card>
            </NavLink>
        </Grid>
    );
}

export default Category;