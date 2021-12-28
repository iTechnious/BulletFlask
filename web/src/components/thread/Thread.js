import { Button, Card, CardActions, CardContent, Grid, Typography } from '@mui/material';
import React from 'react';

const Thread = ({ data }) => {
    return (
        <Card className="thread" sx={{ marginTop: '20px' }}>
            <CardContent>
                <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                    Thread
                </Typography>

                <Typography variant="h5">{ data.name }</Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Ansehen</Button>
            </CardActions>
        </Card>
    );
}

export default Thread;