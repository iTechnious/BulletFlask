import { Button, Card, CardActions, CardContent, Grid, Typography } from '@mui/material';
import React from 'react';
import './Category.css';

const Category = ({ data }) => {
    return (
        <Grid item xs={6}>
            <Card className="category">
                <CardContent>
                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                        Kategorie
                    </Typography>
                    
                    <Typography variant="h5">{ data.name }</Typography>
                    
                    <Typography variant="body2">
                        Beschreibung
                    </Typography>
                </CardContent>
                <CardActions>
                    <Button size="small">Ansehen</Button>
                </CardActions>
            </Card>
        </Grid>
    );
}

export default Category;