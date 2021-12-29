import { Button, Card, CardActions, CardContent, Typography } from '@mui/material';
import React from 'react';
import {t} from "i18next";

const Thread = ({ data }) => {
    return (
        <Card className="thread" sx={{ marginTop: '20px' }}>
            <CardContent>
                <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                    {t('THREAD')}
                </Typography>

                <Typography variant="h5">{ data.name }</Typography>
            </CardContent>
            <CardActions>
                <Button size="small">{t("VIEW")}</Button>
            </CardActions>
        </Card>
    );
}

export default Thread;