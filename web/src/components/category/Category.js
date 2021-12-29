import { Button, Card, CardActions, CardContent, Grid, Typography } from '@mui/material';
import React from 'react';
import {t} from "i18next";

const Category = ({ data }) => {
    return (
        <Grid item xs={6}>
            <Card className="category">
                <CardContent>
                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                        {t("CATEGORY")}
                    </Typography>
                    
                    <Typography variant="h5">{ data.name }</Typography>

                </CardContent>
                <CardActions>
                    <Button size="small">{t("VIEW")}</Button>
                </CardActions>
            </Card>
        </Grid>
    );
}

export default Category;