import { Card, CardContent, Grid, Typography } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';

const Category = ({ data, renew }) => {
    const { t } = useTranslation();

    return (
        <Grid item xs={6}>
            <Card className="category" sx={{ padding: '10px', marginBottom: '20px' }} onClick={ ()=>{ renew(data.id) } } style={ {cursor: "pointer"} }>
                <CardContent>
                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                        { t('CATEGORY') }
                    </Typography>

                    <Typography variant="h5">{ data.name }</Typography>
                </CardContent>
            </Card>
        </Grid>
    );
}

export default Category;