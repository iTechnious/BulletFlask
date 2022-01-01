import { Card, CardContent, Grid, Typography } from '@mui/material';
import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Category = ({ data }) => {
    const { t } = useTranslation();

    return (
        <Grid item xs={6}>
            <Link to="/" style={{ textDecoration: 'inherit' }}>
                <Card className="category" sx={{ padding: '10px', marginBottom: '20px' }}>
                    <CardContent>
                        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                            { t('CATEGORY') }
                        </Typography>
                        
                        <Typography variant="h5">{ data.name }</Typography>
                    </CardContent>
                </Card>
            </Link>
        </Grid>
    );
}

export default Category;