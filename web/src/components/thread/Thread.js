import { Card, CardContent, Typography } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';

const Thread = ({ data, renew }) => {
    const { t } = useTranslation();
    
    return (
        <Card className="thread" sx={{ padding: '10px', marginTop: '20px' }} onClick={ ()=>{ renew(data.id) } } style={ {cursor: "pointer"} }>
            <CardContent>
                <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                    { t('THREAD') }
                </Typography>

                <Typography variant="h5">{ data.name }</Typography>
            </CardContent>
        </Card>
    );
}

export default Thread;