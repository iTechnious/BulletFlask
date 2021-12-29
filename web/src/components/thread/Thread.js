import { Card, CardContent, Typography } from '@mui/material';
import React from 'react';
import {t} from "i18next";
import { Link } from 'react-router-dom';

const Thread = ({ data }) => {
    return (
        <Link to="/" style={{ textDecoration: 'inherit' }}>
            <Card className="thread" sx={{ padding: '10px', marginTop: '20px' }}>
                <CardContent>
                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                        { t('THREAD') }
                    </Typography>

                    <Typography variant="h5">{ data.name }</Typography>
                </CardContent>
            </Card>
        </Link>
    );
}

export default Thread;